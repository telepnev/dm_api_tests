import pytest
import structlog
from faker import Faker

from restclient.configuration import Configuration as DmApiConfiguration
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
        ("valid_user", "valid_user@mail.com", "123456", 201),

        # Negative
        ("", "user@mail.com", "123456", 400),  # пустой login
        ("user2", "invalid-email", "123456", 400),  # невалидный email
        ("user3", "user3@mail.com", "123", 400),  # короткий пароль
    ],
)
def test_post_v1_account_parametrized(login, email, password, expected_status):
    dm_api_configuration = DmApiConfiguration(host="http://185.185.143.231:5051", disable_logs=False)
    account = DmApiAccount(configuration=dm_api_configuration)

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

    response = account.account_api.post_v1_account(json_data=json_data)
    assert response.status_code == expected_status, response.text
