import requests

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

    def delete_v1_account_login(self, token):
        """
        Logout as current user
        :return:
        """
        headers = {
            'accept': 'text/plain',
            'X-Dm-Auth-Token': f'{token}',
        }
        response = self.delete(
            path=f'/v1/account/login',
            headers=headers
        )
        return response

    def delete_v1_account_login_all(self, token):
        """
        Logout from every device
        :return:
        """
        headers = {
            'accept': 'text/plain',
            'X-Dm-Auth-Token': f'{token}',
        }
        response = self.delete(
            path=f'/v1/account/login/all',
            headers=headers
        )
        return response
