from json import loads
from faker import Faker

from dm_api_account.apis.account_api import AccountApi
from dm_api_account.apis.login_api import LoginApi
from api_mailhog.apis.mailhog_api import MailhogApi
import structlog

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(
            indent=4,
            ensure_ascii=True,
            # sort_keys=True,
            # separators=(',', ':')
        )
    ]
)


def test_post_v1_account():
    account_api = AccountApi(host="http://185.185.143.231:5051")
    login_api = LoginApi(host="http://185.185.143.231:5051")
    mailhog_api = MailhogApi(host="http://185.185.143.231:5025")

    faker = Faker()
    # login = faker.name().replace(" ", "")
    # email = f"{login}@mail.com"
    login = "evgen123"
    email = "evgen123@email.ru"

    password = "12345678"

    # Регистрация пользователя
    json_data = {
        'login': login,
        'email': email,
        'password': password,
    }

    response = account_api.post_v1_account(json_data=json_data)
    assert response.status_code == 201, f"Пользователь не был создан {response.text}"

    # Получить письма из почтового ящика
    response = mailhog_api.get_api_v2_messages()
    assert response.status_code == 200, "Письмо не получено"

    # Получить активационный токен

    token = get_activation_token_by_login(login, response)

    assert token is not None, f"Токен для пользователя {login} не был получен"

    # Активация пользователя
    response = account_api.put_v1_account_token(token=token)

    assert response.status_code == 200, "Пользователь не активирован"

    # Авторизация
    json_data = {
        'login': login,
        'password': password,
        'rememberMe': True,
    }

    response = login_api.post_v1_account_login(json_data=json_data)

    assert response.status_code == 200, "Пользователь не авторизован"


def get_activation_token_by_login(login, response):
    token = None
    for item in response.json()['items']:
        user_data = loads(item['Content']['Body'])
        user_login = user_data["Login"]

        if user_login == login:
            print(f"Login {user_login}")
            token = user_data.get("ConfirmationLinkUrl").split("/")[-1]
    return token
