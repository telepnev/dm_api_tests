from dm_api_account.models.general_error import GeneralError


def test_post_v1_account_errors(
        account_helper
):
    token = "00-a08dfec8d0348b161fe71a3ea25de07b-5c17e47a66429927-01"

    response = account_helper.activate_user_by_token_raw(token)

    assert response.status_code == 400

    error = GeneralError.model_validate(response.json())

    assert error.status == 400
    assert error.title == "One or more validation errors occurred."
    assert "token" in error.errors
    assert "Invalid value for field token" in error.errors["token"]


