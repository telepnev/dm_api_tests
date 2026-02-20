from dm_api_account.models.general_error import GeneralError


def test_put_v1_account_activation_expired_token(
        account_helper,
        prepare_user
):
    login = prepare_user.login
    password = prepare_user.password
    email = prepare_user.email

    # Только регистрация
    account_helper.register_user(
        login=login,
        email=email,
        password=password
    )

    expired_token = "fdd84346-dccf-464f-ad1c-81672d846781"
    response = account_helper.activate_user_by_token_raw(expired_token)
    assert response.status_code == 410

    error = GeneralError.model_validate(response.json())
    assert error.title == (
        "Activation token is invalid! "
        "Address the technical support for further assistance"
    )
    #assert error.traceId is not None

