from json import loads

import pytest
from faker import Faker

from api_mailhog.apis.mailhog_api import MailhogApi
from dm_api_account.apis.account_api import AccountApi


@pytest.mark.parametrize(
    "token_modifier, expected_status",
    [
        pytest.param("valid", 200),
        pytest.param("invalid", 400),
        pytest.param("empty", 404),
    ],
)
def test_put_v1_account_activation(token_modifier, expected_status):
    account_api = AccountApi(host="http://185.185.143.231:5051")
    mailhog_api = MailhogApi(host="http://185.185.143.231:5025")

    faker = Faker()
    login = faker.name().replace(" ", "")
    email = f"{login}@mail.com"
    password = "12345678"

    #  регистрация

    response = account_api.post_v1_account(json_data={
        "login": login,
        "email": email,
        "password": password,
    })
    assert response.status_code == 201

    response = mailhog_api.get_api_v2_messages()
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

    response = account_api.put_v1_account_token(token=token)

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