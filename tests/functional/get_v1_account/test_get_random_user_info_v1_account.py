def test_get_v1_account(
        account_helper,
        prepare_user,
        auth_with_cred_account_helper
):

    login = prepare_user.login
    password = prepare_user.password
    email = prepare_user.email

    account_helper.register_new_user(
        login=login,
        email=email,
        password=password
    )

    auth_user = auth_with_cred_account_helper(login, password)
    user = auth_user.get_current_user()

    assert user.resource.login == login
    assert "Player" in user.resource.roles
    assert user.resource.rating.enabled is True
