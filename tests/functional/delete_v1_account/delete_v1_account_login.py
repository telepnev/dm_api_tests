

def test_delete_v1_account_login(auth_account_helper,account_helper):
    response = auth_account_helper.dm_account_api.account_api.get_v1_account()
    token = response.headers.get("X-Dm-Auth-Token")
    response = account_helper.dm_account_api.login_api.delete_v1_account_login(token)

    assert response.status_code == 204

