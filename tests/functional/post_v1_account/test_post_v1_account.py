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

@pytest.fixture
def mailhog_api():
    mailhog_configuration = MailhogConfiguration(host="http://185.185.143.231:5025", disable_logs=True)
    mailhog_client = MailHogApi(configuration=mailhog_configuration)
    return mailhog_client

@pytest.fixture
def account_api():
    dm_api_configuration = DmApiConfiguration(host="http://185.185.143.231:5051", disable_logs=False)
    account = DmApiAccount(configuration=dm_api_configuration)
    return account

@pytest.fixture
def account_helper(account_api, mailhog_api):
    account_helper = AccountHelper(dm_account_api=account_api, mailhog=mailhog_api)
    return account_helper

@pytest.fixture
def prepare_user():
    faker = Faker()
    login = faker.name().replace(" ", "")
    email = f"{login}@mail.com"
    password = "12345678"

    # создаем юзера через namedtuple, быстрый питанячий класс
    User = namedtuple("User", ["login", "email", "password"])
    user = User(login=login, email=email, password=password)
    return user


def test_post_v1_account(account_helper,prepare_user):


    account_helper.register_new_user(
        login=prepare_user.login,
        email=prepare_user.email,
        password=prepare_user.password
    )
    account_helper.user_login(
        login=prepare_user.login,
        password=prepare_user.password)
