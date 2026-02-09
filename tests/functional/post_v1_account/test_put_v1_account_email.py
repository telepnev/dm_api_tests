from json import loads

import structlog
from faker import Faker

from restclient.configuration import Configuration as DmApiConfiguration
from restclient.configuration import Configuration as MailhogConfiguration
from services.api_mailhog import MailHogApi
from services.dm_api_account import DmApiAccount
from tests.functional.post_v1_account.test_post_v1_account import get_activation_token_by_login

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


def test_put_v1_account_email():
    dm_api_configuration = DmApiConfiguration(host="http://185.185.143.231:5051", disable_logs=False)
    mailhog_configuration = MailhogConfiguration(host="http://185.185.143.231:5025", disable_logs=True)

    account = DmApiAccount(configuration=dm_api_configuration)
    mailhog = MailHogApi(configuration=mailhog_configuration)

    faker = Faker()

    login = faker.name().replace(" ", "")
    email = f"{login}@mail.com"
    password = "12345678"
    new_email = f"updated_{email}"

    # Регистрируемся
    json_data = {
        'login': login,
        'email': email,
        'password': password,
    }

    response = account.account_api.post_v1_account(json_data=json_data)
    assert response.status_code == 201, f"Пользователь не был создан {response.text}"

    # Получаем активационный токен и активируем
    response = mailhog.mailhogApi_api.get_api_v2_messages()
    assert response.status_code == 200, "Письмо не получено"

    token = get_activation_token_by_login(login, response)
    assert token is not None, f"Токен для пользователя {login} не был получен"

    response = account.account_api.put_v1_account_token(token=token)
    assert response.status_code == 200, "Пользователь не активирован"

    # Заходим
    json_data = {
        'login': login,
        'password': password,
        'rememberMe': True,
    }

    response = account.login_api.post_v1_account_login(json_data=json_data)
    assert response.status_code == 200, "Пользователь не авторизован"

    # Меняем емейл
    json_data = {
        "login": login,
        "password": password,
        "email": new_email
    }

    response = account.account_api.put_v1_account_change_mail(json_data=json_data)
    assert response.status_code == 200, f"Пользователю {login} не удалось изменить почту"

    # Пытаемся войти, получаем 403
    json_data = {
        'login': login,
        'password': password,
        'rememberMe': True,
    }

    response = account.login_api.post_v1_account_login(json_data=json_data)
    assert response.status_code == 403, "Ожидалась ошибка 403, т.к. пользователь не подтвердил смену почты"

    # На почте находим токен по новому емейлу для подтверждения смены емейла
    response = mailhog.mailhogApi_api.get_api_v2_messages()
    assert response.status_code == 200, "Письмо не получено"

    token = get_activation_token_by_email(new_email, response)
    assert token is not None, f"Токен для пользователя {login} не был получен"

    # Активируем этот токен
    response = account.account_api.put_v1_account_token(token=token)
    assert response.status_code == 200, "Пользователь не активирован"

    # Логинимся
    json_data = {
        'login': login,
        'password': password,
        'rememberMe': True,
    }

    response = account.login_api.post_v1_account_login(json_data=json_data)
    assert response.status_code == 200, "Пользователь не авторизован"


def get_activation_token_by_email(email, response):
    token = None
    for item in response.json()['items']:
        user_data = loads(item['Content']['Body'])
        emails = item['Content']['Headers']['To']

        if email in emails:
            token = user_data.get("ConfirmationLinkUrl").split("/")[-1]

    return token
