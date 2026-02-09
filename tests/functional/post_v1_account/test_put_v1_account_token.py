from json import loads

import pytest
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


@pytest.mark.parametrize(
    "token_modifier, expected_status",
    [
        pytest.param("valid", 200),
        pytest.param("invalid", 400),
        pytest.param("empty", 404),
    ],
)
def test_put_v1_account_activation(token_modifier, expected_status):
    dm_api_configuration = DmApiConfiguration(host="http://185.185.143.231:5051", disable_logs=False)
    mailhog_configuration = MailhogConfiguration(host="http://185.185.143.231:5025", disable_logs=True)

    account = DmApiAccount(configuration=dm_api_configuration)
    mailhog = MailHogApi(configuration=mailhog_configuration)

    faker = Faker()
    login = faker.name().replace(" ", "")
    email = f"{login}@mail.com"
    password = "12345678"

    #  регистрация
    response = account.account_api.post_v1_account(json_data={
        "login": login,
        "email": email,
        "password": password,
    })
    assert response.status_code == 201

    response = mailhog.mailhogApi_api.get_api_v2_messages()
    assert response.status_code == 200

    valid_token = get_activation_token_by_login(login, response)
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


def get_activation_token_by_login(login, response):
    token = None
    for item in response.json()['items']:
        user_data = loads(item['Content']['Body'])
        user_login = user_data["Login"]

        if user_login == login:
            print(f"Login {user_login}")
            token = user_data.get("ConfirmationLinkUrl").split("/")[-1]
    return token
