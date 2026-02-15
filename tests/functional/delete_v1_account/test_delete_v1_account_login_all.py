def test_delete_v1_account_login_204(auth_account_helper,account_helper):
    response = auth_account_helper.dm_account_api.account_api.get_v1_account()
    token = response.headers.get("X-Dm-Auth-Token")
    response = account_helper.dm_account_api.login_api.delete_v1_account_login_all(token)

    assert response.status_code == 204, response.text


def test_delete_v1_account_login_401(auth_account_helper,account_helper):
    token = "Failtoken777111"
    response = account_helper.dm_account_api.login_api.delete_v1_account_login_all(token)

    assert response.status_code == 401, response.text