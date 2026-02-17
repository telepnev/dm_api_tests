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

    def delete_v1_account_login(self, headers: dict | None = None):
        """
        Logout as current user
        :return:
        """

        response = self.delete(
            path='/v1/account/login',
            headers=headers
        )
        return response

    def delete_v1_account_login_all(self, headers: dict | None = None):
        """
        Logout from every device
        :return:
        """
        response = self.delete(
            path='/v1/account/login/all',
            headers=headers
        )
        return response
