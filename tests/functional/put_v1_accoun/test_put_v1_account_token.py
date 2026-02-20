import pytest

from dm_api_account.models.general_error import GeneralError
from dm_api_account.models.user_envelope import UserEnvelope


@pytest.mark.parametrize(
    "token_type, expected_status",
    [
        ("valid", 200),
        ("invalid", 400),
        ("empty", 404),
    ]
)
def test_put_v1_account_activation(
        token_type,
        expected_status,
        account_helper,
        prepare_user
):

    login = prepare_user.login
    password = prepare_user.password
    email = prepare_user.email

    account_helper.register_new_user(
        login=login,
        email=email,
        password=password
    )

    valid_token = account_helper.get_activation_token_by_login(login)

    token_map = {
        "valid": valid_token,
        "invalid": "invalid-token-123",
        "empty": ""
    }

    token = token_map[token_type]
    response = account_helper.activate_user_by_token_raw(token)

    assert response.status_code == expected_status

    if expected_status == 200:
        user = UserEnvelope.model_validate(response.json())
        assert user.resource.login == login

    elif expected_status == 400:
        error = GeneralError.model_validate(response.json())
        assert error.status == 400
        assert "token" in error.errors

    elif expected_status == 404:
        # 404 может быть без тела
        assert not response.content  # тело пустое