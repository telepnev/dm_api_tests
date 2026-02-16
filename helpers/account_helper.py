import time
from functools import wraps
from json import loads

from services.api_mailhog import MailHogApi
from services.dm_api_account import DmApiAccount


def retry_if_result_none(result):
    """Return True if we should retry (in this case when result is None), False otherwise"""
    return result is None


def retry(retries: int = 3, delay: int = 1, exceptions: tuple = (Exception,)):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None

            for attempt in range(1, retries + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    print(f"Attempt {attempt} failed: {e}")

                    if attempt == retries:
                        raise RuntimeError(
                            f"Failed after {retries} attempts"
                        ) from last_exception

                    time.sleep(delay)

        return wrapper

    return decorator


class AccountHelper:
    def __init__(
            self,
            dm_account_api: DmApiAccount,
            mailhog: MailHogApi
            # mailhog: Optional[MailHogApi] = None
    ):
        self.dm_account_api = dm_account_api
        self.mailhog = mailhog

    def register_new_user(self, login: str, password: str, email: str):
        json_data = {
            'login': login,
            'email': email,
            'password': password,
        }

        # Регистрация пользователя
        response = self.dm_account_api.account_api.post_v1_account(json_data=json_data)
        # assert response.status_code == 201, f"Пользователь не был создан {response.text}"

        # Получить письма из почтового ящика
        response = self.mailhog.mailhog_api.get_api_v2_messages()
        # assert response.status_code == 200, "Письмо не получено"

        # Получить активационный токен
        token = self.get_activation_token_by_login(login=login)
        # assert token is not None, f"Токен для пользователя {login} не был получен"

        # Активация пользователя
        response = self.dm_account_api.account_api.put_v1_account_token(token=token)
        # assert response.status_code == 200, "Пользователь не активирован"

        return response

    def auth_client(self, login: str, password: str):
        response = self.dm_account_api.login_api.post_v1_account_login(
            json_data={"login": login, "password": password})
        token = {
            "x-dm-auth-token": response.headers["x-dm-auth-token"],
        }
        # устанавливаем в headers токен
        self.dm_account_api.account_api.set_headers(token)
        # логинемся
        self.dm_account_api.login_api.set_headers(token)

    def logout_client(self, token: str):
        self.dm_account_api.login_api.delete_v1_account_login(token)

    def logout_client_all(self, token: str):
        self.dm_account_api.login_api.delete_v1_account_login_all(token)

    def change_password(self,
                        login: str,
                        password: str,
                        email: str,
                        new_password: str
                        ):
        # логинемся
        response = self.dm_account_api.login_api.post_v1_account_login(
            json_data={"login": login, "password": password})
        # инициируем сброс пароля
        response = self.dm_account_api.account_api.post_v1_account_reset_password(
            json_data={"login": login, "email": email})
        assert response.status_code == 200, "Пользователь не смог сбросить пароль"
        # берем токен из письма
        token = self.get_conferm_token_by_login(login=login)
        assert token is not None, "Не смогли получить token"

        # меняем пароль
        response = self.dm_account_api.account_api.put_v1_account_change_password(
            json_data={
                "login": login,
                "token": token,
                "oldPassword": password,
                "newPassword": new_password,
            })
        return response

    @retry(retries=5, delay=15)
    # старье
    # @retry(stop_max_attempt_number=5,retry_on_result=retry_if_result_none, wait_fixed=1000)
    # новое
    # @retry(stop=stop_after_attempt(3), wait=wait_fixed(1))
    def get_activation_token_by_login(self, login):
        token = None
        # Получить письма из почтового ящика
        response = self.mailhog.mailhog_api.get_api_v2_messages()

        for item in response.json()['items']:
            user_data = loads(item['Content']['Body'])
            user_login = user_data["Login"]

            if user_login == login:
                print(f"Login {user_login}")
                token = user_data.get("ConfirmationLinkUrl").split("/")[-1]
        return token

    def get_conferm_token_by_login(self, login):
        token = None
        # Получить письма из почтового ящика
        response = self.mailhog.mailhog_api.get_api_v2_messages()

        for item in response.json()['items']:
            user_data = loads(item['Content']['Body'])
            user_login = user_data["Login"]

            if user_login == login:
                print(f"Login {user_login}")
                link = user_data.get("ConfirmationLinkUri")
                if link:
                    token = link.split("/")[-1]
                print(f"TOKEN ====================={token}")
        return token

    # Авторизация в систему
    def user_login(self, login: str, password: str, remember_me: bool = True):
        json_data = {
            'login': login,
            'password': password,
            'rememberMe': remember_me
        }

        response = self.dm_account_api.login_api.post_v1_account_login(json_data=json_data)
        # assert response.status_code == 200, "Пользователь не авторизован"

        return response

    def email_change_confirmation_by_new_email(self, new_email: str):
        # На почте находим токен по новому емейлу для подтверждения смены емейла
        response = self.mailhog.mailhog_api.get_api_v2_messages()
        # assert response.status_code == 200, "Письмо не получено"
        token = self.get_activation_token_by_email(new_email, response)
        assert token is not None, f"Токен не найден {new_email}"
        # Активируем этот токен
        response = self.dm_account_api.account_api.put_v1_account_token(token=token)
        # assert response.status_code == 200, "Пользователь не активирован"

        return response

    @staticmethod
    def get_activation_token_by_email(email, response):
        token = None
        for item in response.json()['items']:
            user_data = loads(item['Content']['Body'])
            emails = item['Content']['Headers']['To']

            if email in emails:
                token = user_data.get("ConfirmationLinkUrl").split("/")[-1]

        return token

    def get_current_user(self):
        response = self.dm_account_api.account_api.get_v1_account()
        return response

    def logout(self, token: str | None = None):
        response = self.dm_account_api.login_api.delete_v1_account_login(token)
        return response

    def logout_all(self, token: str | None = None):
        response = self.dm_account_api.login_api.delete_v1_account_login_all(token)
        return response

    # Изменение почты
    def user_change_email(self, login: str, password: str, new_email: str):
        # Меняем емейл
        json_data = {
            "login": login,
            "password": password,
            "email": new_email
        }

        response = self.dm_account_api.account_api.put_v1_account_change_mail(json_data=json_data)
        # assert response.status_code == 200, f"Пользователю {login} не удалось изменить почту"

        return response
