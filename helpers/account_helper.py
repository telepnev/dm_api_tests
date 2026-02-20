import json
import re
import time
from functools import wraps
from json import loads, JSONDecodeError

from requests import JSONDecodeError

from dm_api_account.models.change_email import ChangeEmail
from dm_api_account.models.change_password import ChangePassword
from dm_api_account.models.login_credentials import LoginCredentials
from dm_api_account.models.registration import Registration
from dm_api_account.models.reset_password import ResetPassword
from dm_api_account.models.user_envelope import UserEnvelope


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
    def __init__(self, dm_account_api, mailhog):
        self.dm_account_api = dm_account_api
        self.mailhog = mailhog
        self.token = None

    def register_new_user(self, login: str, password: str, email: str):
        registration = Registration(
            login=login,
            password=password,
            email=email
        )
        # Регистрация пользователя
        response = self.dm_account_api.account_api.post_v1_account(registration=registration)
        assert response.status_code == 201, f"Пользователь не был создан {response.text}"

        # Получить письма из почтового ящика
        response = self.mailhog.mailhog_api.get_api_v2_messages()
        assert response.status_code == 200, "Письмо не получено"

        # Получить активационный токен
        start_time = time.time()
        token = self.get_activation_token_by_login(login=login)
        end_time = time.time()
        assert end_time - start_time < 5, "Время активации превышено"
        assert token is not None, f"Токен для пользователя {login} не был получен"

        # Активация пользователя
        response = self.dm_account_api.account_api.put_v1_account_token(token=token)
        # assert response.status_code == 200, "Пользователь не активирован"

        model = None
        if response.status_code == 200:
            model = UserEnvelope(**response.json())

        return response, model

    def register_new_user_without_activetion(self, login: str, password: str, email: str):
        registration = Registration(
            login=login,
            password=password,
            email=email
        )
        # Регистрация пользователя
        response = self.dm_account_api.account_api.post_v1_account(registration=registration)
        assert response.status_code == 201, f"Пользователь не был создан {response.text}"

        # Получить письма из почтового ящика
        response = self.mailhog.mailhog_api.get_api_v2_messages()
        assert response.status_code == 200, "Письмо не получено"

        # Получить активационный токен
        start_time = time.time()
        token = self.get_activation_token_by_login(login=login)
        end_time = time.time()
        assert end_time - start_time < 3, "Время активации превышено"
        assert token is not None, f"Токен для пользователя {login} не был получен"

        return response

    def activate_user_by_token(self, token: str):
        response = self.dm_account_api.account_api.put_v1_account_token(token=token)

        return response

    def auth_client(self, login: str, password: str):
        response, model, token = self.user_login(
            login=login,
            password=password
        )

        assert response.status_code == 200
        assert token is not None

        self.token = token

        return response

    def reset_password(self, login: str, email: str):
        """
        Initiate password reset flow
        """
        payload = ResetPassword(
            login=login,
            email=email
        ).model_dump(exclude_none=True, by_alias=True)

        response = self.dm_account_api.account_api.post_v1_account_password(
            json=payload
        )

        return response

    def change_password_by_token(
            self,
            login: str,
            token: str,
            old_password: str,
            new_password: str
    ):
        """
        Change user password using confirmation token
        """
        payload = ChangePassword(
            login=login,
            token=token,
            old_password=old_password,
            new_password=new_password
        ).model_dump(exclude_none=True, by_alias=True)

        response = self.dm_account_api.account_api.put_v1_account_password(
            json=payload
        )

        return response

    def change_password(
            self,
            login: str,
            email: str,
            old_password: str,
            new_password: str
    ):
        # Arrange
        response = self.reset_password(login=login, email=email)
        assert response.status_code == 200

        token = self.get_conferm_token_by_login(login)
        assert token is not None

        # Act
        response = self.change_password_by_token(
            login=login,
            token=token,
            old_password=old_password,
            new_password=new_password
        )

        return response

    @retry(retries=5, delay=5)
    def get_activation_token_by_login(self, login: str) -> str | None:
        """
        Extract activation token from MailHog by user login.
        Retries if token not found.
        """
        response = self.mailhog.mailhog_api.get_api_v2_messages()
        messages = response.json().get("items", [])

        for item in messages:
            body = item.get("Content", {}).get("Body")

            if not body:
                continue

            # Ищем JSON в теле письма (lazy match)
            json_match = re.search(r"\{.*?\}", body)
            if not json_match:
                continue

            try:
                user_data = json.loads(json_match.group())
            except (json.JSONDecodeError, TypeError):
                continue

            # Проверяем логин
            if user_data.get("Login") != login:
                continue

            confirmation_url = user_data.get("ConfirmationLinkUrl")
            if not confirmation_url:
                continue

            return confirmation_url.split("/")[-1]

        return None

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

    def user_login(
            self,
            login: str,
            password: str,
            remember_me: bool = True
    ):
        login_credentials = LoginCredentials(
            login=login,
            password=password,
            remember_me=remember_me
        )

        response = self.dm_account_api.login_api.post_v1_account_login(
            login_credentials=login_credentials,
            validate_response=False
        )

        model = None
        token = None

        if response.status_code == 200:
            model = UserEnvelope(**response.json())
            token = response.headers.get("X-Dm-Auth-Token")

        return response, model, token

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

        for item in response.json().get('items', []):
            try:
                headers = item.get('Content', {}).get('Headers', {})
                emails = headers.get('To', [])

                # Сначала проверяем получателя
                if email not in emails:
                    continue

                body = item.get('Content', {}).get('Body', '')

                # Потом пробуем парсить JSON
                user_data = loads(body)

                confirmation_url = user_data.get("ConfirmationLinkUrl")
                if confirmation_url:
                    token = confirmation_url.split("/")[-1]
                    break

            except (JSONDecodeError, KeyError, AttributeError):
                continue

        return token

    def get_current_user(self):
        headers = None

        if self.token:
            headers = {"X-Dm-Auth-Token": self.token}

        return self.dm_account_api.account_api.get_v1_account(
            headers=headers
        )

    def logout(self, token: str | None = None):
        auth_token = token or self.token
        headers = {"X-Dm-Auth-Token": auth_token}
        return self.dm_account_api.login_api.delete_v1_account_login(
            headers=headers
        )

    def logout_all(self, token: str | None = None):
        auth_token = token or self.token
        headers = {"X-Dm-Auth-Token": auth_token}

        return self.dm_account_api.login_api.delete_v1_account_login_all(headers=headers)

    # Изменение почты
    def user_change_email(self, login: str, password: str, new_email: str):
        # Меняем емейл
        change_mail = ChangeEmail(
            login=login,
            password=password,
            email=new_email
        )

        response = self.dm_account_api.account_api.put_v1_account_mail(change_mail=change_mail)
        # assert response.status_code == 200, f"Пользователю {login} не удалось изменить почту"

        return response

    def activate_user_by_token(self, token: str):
        response = self.dm_account_api.account_api.put_v1_account_token(token)
        # для проверок на статус коды, если все ок  вернем DTO, нет то json
        model = None
        if response.status_code == 200:
            model = UserEnvelope(**response.json())
        return response, model
