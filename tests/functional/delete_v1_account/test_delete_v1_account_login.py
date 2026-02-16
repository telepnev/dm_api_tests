

def test_delete_v1_account_login_204(auth_account_helper):
    response = auth_account_helper.get_current_user()
    token = response.headers.get("X-Dm-Auth-Token")
    response = auth_account_helper.logout(token)

    assert response.status_code == 204, response.text


def test_delete_v1_account_login_401(auth_account_helper):
    token = "Failtoken777111"
    response = auth_account_helper.logout(token)

    assert response.status_code == 401, response.text

