"""
auth_account_helper - авторизованный клиент
account_helper -не авторизованный клиент
"""




def test_get_v1_account_auth(auth_account_helper):
    response =auth_account_helper.dm_account_api.account_api.get_v1_account()
    assert response.status_code == 200

def test_get_v1_account_no_auth(account_helper):
    response = account_helper.dm_account_api.account_api.get_v1_account()
    assert response.status_code == 401