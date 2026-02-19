import pytest
from faker import Faker
from pydantic import ValidationError

from helpers.account_helper import AccountHelper
from restclient.configuration import Configuration as DmApiConfiguration
from restclient.configuration import Configuration as MailhogConfiguration
from services.api_mailhog import MailHogApi
from services.dm_api_account import DmApiAccount


@pytest.mark.parametrize(
    "login, email, password, is_valid_data",
    [
        # Позитивный кейс — все данные валидны и проходят Pydantic-модель Registration
        ("valid_user", "valid_user@mail.com", "12345678", True),

        # Негативные кейсы. Здесь мы проверяем уже валидацию Pydantic, а не ответ API.
        ("", "user@mail.com", "12345678", False),          # пустой login
        ("user2", "invalid-email", "12345678", False),     # невалидный email
        ("user3", "user3@mail.com", "123", False),         # короткий пароль
    ],
)
def test_post_v1_account_parametrized(login, email, password, is_valid_data):
    """
    Тест адаптирован под новые Pydantic-модели:
    - Для валидных данных ожидаем успешную регистрацию и активацию пользователя.
    - Для невалидных данных ожидаем ValidationError на этапе создания модели Registration.
    """
    faker = Faker()

    dm_api_configuration = DmApiConfiguration(host="http://185.185.143.231:5051", disable_logs=False)
    mailhog_configuration = MailhogConfiguration(host="http://185.185.143.231:5025", disable_logs=True)

    account = DmApiAccount(configuration=dm_api_configuration)
    mailhog = MailHogApi(configuration=mailhog_configuration)

    account_helper = AccountHelper(dm_account_api=account, mailhog=mailhog)

    # Генерируем уникальные данные ТОЛЬКО для позитивного кейса,
    # чтобы не ловить конфликты по логину/почте.
    if is_valid_data:
        login = f"{login}_{faker.name().replace(' ', '')}"
        email = f"{faker.name().replace(' ', '')}_{email}"

    if is_valid_data:
        # Для валидных данных helper должен отработать без ошибок
        response = account_helper.register_new_user(login=login, email=email, password=password)
        # register_new_user — полный цикл, внутри уже есть проверки статуса.
        # Здесь оставляем дополнительную проверку, что активация прошла успешно.
        assert response.status_code == 200, "Ожидается успешная активация пользователя"
    else:
        # Для невалидных данных ожидаем, что Pydantic-модель бросит исключение
        with pytest.raises(ValidationError):
            account_helper.register_new_user(login=login, email=email, password=password)
