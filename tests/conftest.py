from collections import namedtuple

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


@pytest.fixture(scope="session")
def mailhog_api():
    mailhog_configuration = MailhogConfiguration(
        host="http://185.185.143.231:5025",
        disable_logs=True
    )
    mailhog_client = MailHogApi(configuration=mailhog_configuration)
    return mailhog_client


@pytest.fixture(scope="session")
def account_api():
    dm_api_configuration = DmApiConfiguration(
        host="http://185.185.143.231:5051",
        disable_logs=False
    )
    account = DmApiAccount(configuration=dm_api_configuration)
    return account


@pytest.fixture(scope="session")
def account_helper(account_api, mailhog_api):
    account_helper = AccountHelper(
        dm_account_api=account_api,
        mailhog=mailhog_api
    )

    return account_helper


@pytest.fixture(scope="session")
def auth_account_helper(mailhog_api):
    dm_api_configuration = DmApiConfiguration(
        host="http://185.185.143.231:5051",
        disable_logs=False
    )
    account = DmApiAccount(configuration=dm_api_configuration)
    account_helper = AccountHelper(
        dm_account_api=account,
        mailhog=mailhog_api)

    account_helper.auth_client(
        login="StevenWebb",
        password="@780bwSqMl"

    )

    return account_helper


@pytest.fixture
def auth_with_cred_account_helper(mailhog_api):
    dm_api_configuration = DmApiConfiguration(
        host="http://185.185.143.231:5051",
        disable_logs=False
    )
    account = DmApiAccount(configuration=dm_api_configuration)

    def _auth(login: str, password: str):
        account_helper = AccountHelper(
            dm_account_api=account,
            mailhog=mailhog_api
        )
        account_helper.auth_client(
            login=login,
            password=password
        )
        return account_helper

    return _auth


@pytest.fixture
def prepare_user():
    faker = Faker()
    login = faker.name().replace(" ", "")
    email = f"{login}@mail.com"
    password = "12345678"
    new_password = faker.password(
        length=10,
        # special_chars=True,
        digits=True,
        upper_case=True,
        lower_case=True
    )

    # создаем юзера через namedtuple, быстрый питанячий класс
    User = namedtuple("User", [
        "login",
        "email",
        "password",
        "new_password"
    ])
    user = User(
        login=login,
        email=email,
        password=password,
        new_password=new_password
    )

    return user
