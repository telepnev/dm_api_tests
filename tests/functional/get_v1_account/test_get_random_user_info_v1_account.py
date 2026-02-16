
def test_get_v1_account(account_helper, prepare_user, auth_with_cred_account_helper):
    login = prepare_user.login
    password = prepare_user.password
    email = prepare_user.email

    # Регистрирую нового пользователя
    account_helper.register_new_user(
        login=login,
        email=email,
        password=password
    )

    # auth
    auth_user = auth_with_cred_account_helper(login, password)
    response = auth_user.dm_account_api.account_api.get_v1_account()

    # get_current_user

    assert response.status_code == 200

    body = response.json()
    resource = body["resource"]

    assert resource["login"] == login
    assert "Player" in resource["roles"]
    assert resource["rating"]["enabled"] is True
