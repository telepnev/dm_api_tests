from json import loads

from services.api_mailhog import MailHogApi
from services.dm_api_account import DmApiAccount


class AccountHelper:
    def __init__(
            self,
            dm_account_api: DmApiAccount,
            mailhog: MailHogApi
            #mailhog: Optional[MailHogApi] = None
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
        #assert response.status_code == 201, f"Пользователь не был создан {response.text}"

        # Получить письма из почтового ящика
        response = self.mailhog.mailhogApi_api.get_api_v2_messages()
       # assert response.status_code == 200, "Письмо не получено"

        # Получить активационный токен
        token = self.get_activation_token_by_login(login=login, response=response)
       # assert token is not None, f"Токен для пользователя {login} не был получен"

        # Активация пользователя
        response = self.dm_account_api.account_api.put_v1_account_token(token=token)
        #assert response.status_code == 200, "Пользователь не активирован"

        return response

    # Авторизация в систему
    def user_login(self, login: str, password: str, remember_me: bool = True):
        json_data = {
            'login': login,
            'password': password,
            'rememberMe': remember_me
        }

        response = self.dm_account_api.login_api.post_v1_account_login(json_data=json_data)
        #assert response.status_code == 200, "Пользователь не авторизован"

        return response

    def email_change_confirmation_by_new_email(self, new_email: str):
        # На почте находим токен по новому емейлу для подтверждения смены емейла
        response = self.mailhog.mailhogApi_api.get_api_v2_messages()
        #assert response.status_code == 200, "Письмо не получено"
        token = self.get_activation_token_by_email(new_email, response)
        assert token is not None, f"Токен не найден {new_email}"
        # Активируем этот токен
        response = self.dm_account_api.account_api.put_v1_account_token(token=token)
        #assert response.status_code == 200, "Пользователь не активирован"

        return response

    @staticmethod
    def get_activation_token_by_login(login, response):
        token = None
        for item in response.json()['items']:
            user_data = loads(item['Content']['Body'])
            user_login = user_data["Login"]

            if user_login == login:
                print(f"Login {user_login}")
                token = user_data.get("ConfirmationLinkUrl").split("/")[-1]
        return token

    @staticmethod
    def get_activation_token_by_email(email, response):
        token = None
        for item in response.json()['items']:
            user_data = loads(item['Content']['Body'])
            emails = item['Content']['Headers']['To']

            if email in emails:
                token = user_data.get("ConfirmationLinkUrl").split("/")[-1]

        return token

    # Изменение почты
    def user_change_email(self, login: str, password: str, new_email: str):
        # Меняем емейл
        json_data = {
            "login": login,
            "password": password,
            "email": new_email
        }

        response = self.dm_account_api.account_api.put_v1_account_change_mail(json_data=json_data)
        #assert response.status_code == 200, f"Пользователю {login} не удалось изменить почту"

        return response
