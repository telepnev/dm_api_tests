def test_get_v1_account_auth(auth_account_helper):
    response = auth_account_helper.get_current_user()
    assert response.status_code == 200


def test_get_v1_account_no_auth(account_helper):
    response = account_helper.get_current_user()
    assert response.status_code == 401
