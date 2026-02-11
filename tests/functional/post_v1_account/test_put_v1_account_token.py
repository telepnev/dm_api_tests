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
    "token_modifier, expected_status",
    [
        pytest.param("valid", 200),
        pytest.param("invalid", 400),
        pytest.param("empty", 404),
    ],
)
def test_put_v1_account_activation(token_modifier, expected_status):
    dm_api_configuration = DmApiConfiguration(host="http://185.185.143.231:5051", disable_logs=True)
    mailhog_configuration = MailhogConfiguration(host="http://185.185.143.231:5025", disable_logs=True)

    account = DmApiAccount(configuration=dm_api_configuration)
    mailhog = MailHogApi(configuration=mailhog_configuration)

    account_helper = AccountHelper(dm_account_api=account, mailhog=mailhog)

    faker = Faker()
    login = faker.name().replace(" ", "")
    email = f"{login}@mail.com"
    password = "12345678"

    #  регистрация
    response = account_helper.register_new_user(login=login, email=email, password=password)
    assert response.status_code == 200

    # нужен ли отдельный метод?? И где его оставить и как сделать
    # получение списка писем
    # response = mailhog.mailhogApi_api.get_api_v2_messages()
    # assert response.status_code == 200
    #
    # valid_token = account_helper.get_activation_token_by_login(login=login, response=response)

    valid_token = account_helper.get_activation_token_by_login(login=login)
    assert valid_token is not None

    #  подготовка токена
    if token_modifier == "valid":
        token = valid_token
    elif token_modifier == "invalid":
        token = "invalid-token-123"
    elif token_modifier == "empty":
        token = ""

    #  активация
    response = account.account_api.put_v1_account_token(token=token)
    assert response.status_code == expected_status

