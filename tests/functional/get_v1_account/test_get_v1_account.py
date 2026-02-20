def test_get_v1_account_auth(auth_account_helper):
    user = auth_account_helper.get_current_user()
    assert user.resource.login == "StevenWebb"


def test_get_v1_account_no_auth(account_helper):
    response = account_helper.get_current_user_raw()
    assert response.status_code == 401
