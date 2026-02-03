from json import loads


from dm_api_account.apis.account_api import AccountApi
from dm_api_account.apis.login_api import LoginApi
from api_mailhog.apis.mailhog_api import MailhogApi


import pytest
from faker import Faker


@pytest.mark.parametrize(
    "activate_user, expected_login_status",
    [
        pytest.param(True, 200),
        pytest.param(False, 403),
    ],
)
def test_post_v1_account_parametrized_flow(activate_user, expected_login_status):
    account_api = AccountApi(host="http://185.185.143.231:5051")
    login_api = LoginApi(host="http://185.185.143.231:5051")
    mailhog_api = MailhogApi(host="http://185.185.143.231:5025")

    faker = Faker()
    login = faker.name().replace(" ", "")
    email = f"{login}@mail.com"
    password = "12345678"


    # регистрация

    response = account_api.post_v1_account(json_data={
        "login": login,
        "email": email,
        "password": password,
    })
    assert response.status_code == 201, "Пользователь не был создан"


    # получить письмо

    response = mailhog_api.get_api_v2_messages()
    assert response.status_code == 200, "Письмо не получено"

    token = get_activation_token_by_login(login, response)
    assert token is not None, "Активационный токен не найден"


    #  активация

    if activate_user:
        response = account_api.put_v1_account_token(token=token)
        assert response.status_code == 200, "Пользователь не активирован"


    # авторизация

    response = login_api.post_v1_account_login(json_data={
        "login": login,
        "password": password,
        "rememberMe": True,
    })

    assert response.status_code == expected_login_status


def get_activation_token_by_login(login, response):
    token = None
    for item in response.json()['items']:
        user_data = loads(item['Content']['Body'])
        user_login = user_data["Login"]

        if user_login == login:
            print(f"Login {user_login}")
            token = user_data.get("ConfirmationLinkUrl").split("/")[-1]
    return token
