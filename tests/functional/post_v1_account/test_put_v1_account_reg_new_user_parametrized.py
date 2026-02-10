import pytest
import structlog
from faker import Faker

from helpers.account_helper import AccountHelper
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


@pytest.mark.parametrize(
    "login, email, password, expected_status",
    [
        # Positive
        ("valid_user", "valid_user@mail.com", "123456", 200),

        # Negative , пока хватит ...
        ("", "user@mail.com", "123456", 400),  # пустой login
        ("user2", "invalid-email", "123456", 400),  # невалидный email
        ("user3", "user3@mail.com", "123", 400),  # короткий пароль
    ],
)
def test_post_v1_account_parametrized(login, email, password, expected_status):
    faker = Faker()

    dm_api_configuration = DmApiConfiguration(host="http://185.185.143.231:5051", disable_logs=False)
    mailhog_configuration = MailhogConfiguration(host="http://185.185.143.231:5025", disable_logs=True)

    account = DmApiAccount(configuration=dm_api_configuration)
    mailhog = MailHogApi(configuration=mailhog_configuration)

    account_helper = AccountHelper(dm_account_api=account, mailhog=mailhog)

    # Генерируем уникальные данные ТОЛЬКО для позитивного кейса
    if expected_status == 200:
        login = f"{login}_{faker.name().replace(" ", "")}"
        email = f"{faker.name().replace(" ", "")}_{email}"

    response = account_helper.register_new_user(login=login, email=email, password=password)
    assert response.status_code == expected_status

    # cgtwfkmyj lkallajd;JA;SJD;
    assert response.status_code == expected_status
