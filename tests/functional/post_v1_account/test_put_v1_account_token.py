import pytest


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

    account_helper.register_new_user_without_activetion(
        login=login,
        email=email,
        password=password
    )

    valid_token = account_helper.get_activation_token_by_login(login)

    if token_type == "valid":
        token = valid_token
    elif token_type == "invalid":
        token = "invalid-token-123"
    else:
        token = ""

    response, user_model = account_helper.activate_user_by_token(token)

    assert response.status_code == expected_status

    if expected_status == 200:
        assert user_model is not None
        assert user_model.resource.login == login
    else:
        assert user_model is None
