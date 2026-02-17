def test_delete_v1_account_login_204(auth_account_helper):
    auth_account_helper.get_current_user()
    response = auth_account_helper.logout()

    assert response.status_code == 204


def test_delete_v1_account_login_401(account_helper):
    token = "Failtoken777111"
    response = account_helper.logout(token)

    assert response.status_code == 401, response.text
