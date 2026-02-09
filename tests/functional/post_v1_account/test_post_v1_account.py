from json import loads

import structlog
from faker import Faker

from restclient.configuration import Configuration as DmApiConfiguration
from restclient.configuration import Configuration as MailhogConfiguration
from services.api_mailhog import MailHogApi
from services.dm_api_account import DmApiAccount

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
    dm_api_configuration = DmApiConfiguration(host="http://185.185.143.231:5051", disable_logs=False)
    mailhog_configuration = MailhogConfiguration(host="http://185.185.143.231:5025", disable_logs=True)

    account = DmApiAccount(configuration=dm_api_configuration)
    mailhog = MailHogApi(configuration=mailhog_configuration)

    faker = Faker()
    login = faker.name().replace(" ", "")
    email = f"{login}@mail.com"
    password = "12345678"

    # login = "evgen123455"
    # email = "evgen123@email.ru"

    # Регистрация пользователя
    json_data = {
        'login': login,
        'email': email,
        'password': password,
    }

    response = account.account_api.post_v1_account(json_data=json_data)
    assert response.status_code == 201, f"Пользователь не был создан {response.text}"

    # Получить письма из почтового ящика
    response = mailhog.mailhogApi_api.get_api_v2_messages()
    assert response.status_code == 200, "Письмо не получено"

    # Получить активационный токен
    token = get_activation_token_by_login(login, response)
    assert token is not None, f"Токен для пользователя {login} не был получен"

    # Активация пользователя
    response = account.account_api.put_v1_account_token(token=token)
    assert response.status_code == 200, "Пользователь не активирован"

    # Авторизация
    json_data = {
        'login': login,
        'password': password,
        'rememberMe': True,
    }

    response = account.login_api.post_v1_account_login(json_data=json_data)
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
