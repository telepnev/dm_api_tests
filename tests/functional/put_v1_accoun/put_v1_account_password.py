def test_change_password_v1_account(account_helper, prepare_user):
    login = prepare_user.login
    password = prepare_user.password
    email = prepare_user.email
    new_password = prepare_user.new_password

    account_helper.register_new_user(
        login=login,
        email=email,
        password=password
    )

    reset_response = account_helper.reset_password(
        login=login,
        email=email
    )

    assert reset_response.status_code == 200

    # Получаем токен из письма
    token = account_helper.get_conferm_token_by_login(login)
    assert token is not None

    change_response = account_helper.change_password_by_token(
        login=login,
        token=token,
        old_password=password,
        new_password=new_password
    )

    assert change_response.status_code == 200

    # Проверяем что можно залогиниться новым паролем
    login_response, login_model, auth_token = account_helper.user_login(
        login=login,
        password=new_password
    )

    assert login_response.status_code == 200
    assert auth_token is not None
