def test_change_password_v1_account(account_helper, prepare_user):
    login = prepare_user.login
    password = prepare_user.password
    email = prepare_user.email
    new_password = prepare_user.new_password

    # Регистрирую нового пользователя
    account_helper.register_new_user(
        login=login,
        email=email,
        password=password
    )
    # Меняем пароль
    response = account_helper.change_password(
        login=login,
        password=password,
        email=email,
        new_password=new_password
    )

    assert response.status_code == 200

    # логинемся
    response = account_helper.user_login(
        login=login,
        password=new_password
    )

    assert response.status_code == 200
