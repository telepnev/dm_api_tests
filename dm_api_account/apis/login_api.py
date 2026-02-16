from restclient.client import RestClient


class LoginApi(RestClient):

    def post_v1_account_login(self, json_data):
        """
        Authenticate via credentials
        :param json_data:
        :return:
        """
        response = self.post(
            path=f'/v1/account/login',
            json=json_data
        )
        return response

    def delete_v1_account_login(self, token: str | None = None):
        """
        Logout as current user
        :return:
        """
        if token:
            headers = {"X-Dm-Auth-Token": token}
        else:
            headers = None  # использовать текущие, нифига не менять

        response = self.delete(
            path=f'/v1/account/login',
            headers=headers
        )
        return response

    def delete_v1_account_login_all(self, token: str | None = None):
        """
        Logout from every device
        :return:
        """
        if token:
            headers = {"X-Dm-Auth-Token": token}
        else:
            headers = None  # использовать текущие, нифига не менять

        response = self.delete(
            path=f'/v1/account/login',
            headers=headers
        )
        return response
