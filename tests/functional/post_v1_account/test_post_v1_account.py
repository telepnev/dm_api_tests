from dm_api_account.models.user_envelope import UserRole


def test_post_v1_account(account_helper, prepare_user):

    login = prepare_user.login
    email = prepare_user.email
    password = prepare_user.password

    response, user_model = account_helper.register_new_user(
        login=login,
        email=email,
        password=password
    )

    assert response.status_code == 200
    assert user_model.resource.login == login
    assert UserRole.GUEST in user_model.resource.roles
    assert user_model.resource.registration is None




