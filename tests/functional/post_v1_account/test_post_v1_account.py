from dm_api_account.models.user_envelope import UserRole


def test_post_v1_account(account_helper, prepare_user):
    login = prepare_user.login
    email = prepare_user.email
    password = prepare_user.password

    response = account_helper.register_new_user(
        login=login,
        email=email,
        password=password
    )

    assert UserRole.GUEST in response.resource.roles
    assert UserRole.PLAYER in response.resource.roles

    account_helper.user_login(
        login=login,
        password=password
    )

