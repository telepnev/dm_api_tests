import pytest


@pytest.mark.parametrize(
    "activate_user, expected_login_status",
    [
        pytest.param(True, 200),
        pytest.param(False, 403),
    ],
)
def test_post_v1_account_parametrized_login(
        activate_user,
        expected_login_status,
        account_helper,
        prepare_user
):
    login = prepare_user.login
    email = prepare_user.email
    password = prepare_user.password

    # регистрация
    register_response = account_helper.register_new_user_without_activetion(
        login=login,
        email=email,
        password=password
    )

    assert register_response.status_code == 200

    if activate_user:
        token = account_helper.get_activation_token_by_login(login)

        activation_response, user_model = (
            account_helper.activate_user_by_token(token)
        )

        assert activation_response.status_code == 200
        assert user_model.resource.login == login

    login_response, login_model, token = account_helper.user_login(
        login=login,
        password=password
    )

    assert login_response.status_code == expected_login_status

    if expected_login_status == 200:
        assert login_model is not None
        assert login_model.resource.login == login

    if expected_login_status == 403:
        assert login_model is None
