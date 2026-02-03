import pytest
from faker import Faker

from dm_api_account.apis.account_api import AccountApi



@pytest.mark.parametrize(
    "login, email, password, expected_status",
    [
        # Positive
        ("valid_user", "valid_user@mail.com", "123456", 201),

        # Negative
        ("", "user@mail.com", "123456", 400),                # пустой login
        ("user2", "invalid-email", "123456", 400),           # невалидный email
        ("user3", "user3@mail.com", "123", 400),             # короткий пароль
    ],
)
def test_post_v1_account_parametrized(login, email, password, expected_status):
    account_api = AccountApi(host="http://185.185.143.231:5051")

    faker = Faker()

    # Чтобы login/email были уникальны
    if login:
        login = f"{login}_{faker.uuid4()}"
    if email and "@" in email:
        email = f"{faker.uuid4()}_{email}"

    json_data = {
        "login": login,
        "email": email,
        "password": password,
    }

    response = account_api.post_v1_account(json_data=json_data)

    assert response.status_code == expected_status, response.text






