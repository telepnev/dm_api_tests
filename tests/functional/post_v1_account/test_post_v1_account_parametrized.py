import pytest


@pytest.mark.parametrize(
    "activate_user, expected_login_status",
    [
        pytest.param(True, 200),
        pytest.param(False, 403),
        pytest.param(True, 400)
    ],
)

@pytest.mark.skip("тест в разработке")
def test_post_v1_account_parametrized_login(
    activate_user,
    expected_login_status,
    account_helper,
    prepare_user
):

    register_response = account_helper.register_new_user(
        login=prepare_user.login,
        email=prepare_user.email,
        password=prepare_user.password
    )
    # т.к. register_new_user метод полного цикла вернет не 201,
    # а 200 из - за self.dm_account_api.account_api.put_v1_account_token
    assert register_response.status_code == 200

    if activate_user:
        activation_response = account_helper.activate_user(
            login=prepare_user.login
        )
        assert activation_response.status_code == 200

    login_response = account_helper.user_login(
        login=prepare_user.login,
        password=prepare_user.password
    )

    assert login_response.status_code == expected_login_status

    response_json = login_response.json()

    if expected_login_status == 200:
        assert "token" in response_json
        assert response_json["token"] is not None
        assert len(response_json["token"]) > 0

    if expected_login_status == 403:
        assert "message" in response_json
        assert "not activated" in response_json["message"].lower()