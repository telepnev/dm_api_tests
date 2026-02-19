def test_put_v1_account_email_change(account_helper, prepare_user):
    login = prepare_user.login
    email = prepare_user.email
    password = "12345678"
    new_email = f"updated_{email}"

    account_helper.register_new_user(
        login=login,
        email=email,
        password=password
    )
    account_helper.user_login(
        login=login,
        password=password
    )

    # меняем почту
    account_helper.user_change_email(
        login=login,
        password=password,
        new_email=new_email
    )

    # Пытаемся войти по старой почте, получаем 403
    response = account_helper.user_login(
        login=login,
        password=password
    )
    assert response.status_code == 403, "Ожидалась ошибка 403, т.к. пользователь не подтвердил смену почты"

    # подтверждаем смену почты
    response = account_helper.email_change_confirmation_by_new_email(new_email=new_email)

    # логинемся
    response = account_helper.user_login(
        login=login,
        password=password
    )
    assert response.status_code == 200, "Пользователь не авторизован"



