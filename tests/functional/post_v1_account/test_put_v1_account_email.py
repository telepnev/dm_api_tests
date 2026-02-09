from json import loads
from faker import Faker

from helpers.account_helper import AccountHelper
# from tests.functional.post_v1_account.test_post_v1_account import get_activation_token_by_login
from restclient.configuration import Configuration as MailhogConfiguration
from restclient.configuration import Configuration as DmApiConfiguration

from services.api_mailhog import MailHogApi
from services.dm_api_account import DmApiAccount

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


def test_put_v1_account_email():
    dm_api_configuration = DmApiConfiguration(host="http://185.185.143.231:5051", disable_logs=True)
    mailhog_configuration = MailhogConfiguration(host="http://185.185.143.231:5025", disable_logs=True)

    account = DmApiAccount(configuration=dm_api_configuration)
    mailhog = MailHogApi(configuration=mailhog_configuration)

    account_helper = AccountHelper(dm_account_api=account, mailhog=mailhog)

    faker = Faker()
    login = faker.name().replace(" ", "")
    email = f"{login}@mail.com"
    password = "12345678"
    new_email = f"updated_{email}"

    account_helper.register_new_user(
        login=login,
        email=email,
        password=password
    )
    account_helper.user_login(
        login=login,
        password=password
    )

    # меняем почту
    account_helper.user_change_email(
        login=login,
        password=password,
        new_email=new_email
    )

    # Пытаемся войти по старой почте, получаем 403
    response = account_helper.user_login(
        login=login,
        password=password
    )
    assert response.status_code == 403, "Ожидалась ошибка 403, т.к. пользователь не подтвердил смену почты"

    # подтверждаем смену почты
    response = account_helper.email_change_confirmation_by_new_email(new_email=new_email)
    assert response.status_code == 200, f"Не удалось подтвердить смену почты {new_email}"

    # логинемся
    response = account_helper.user_login(
        login=login,
        password=password
    )
    assert response.status_code == 200, "Пользователь не авторизован"

