from requests import Response

from dm_api_account.models.change_email import ChangeEmail
from dm_api_account.models.change_password import ChangePassword
from dm_api_account.models.login_credentials import LoginCredentials
from dm_api_account.models.registration import Registration
from dm_api_account.models.reset_password import ResetPassword
from restclient.client import RestClient


class AccountApi(RestClient):

    def post_v1_account(self, registration: Registration, **kwargs) -> Response:
        """
        Register new user
        :param json_data:
        :return:
        """
        response = self.post(
            path=f'/v1/account',
            json=registration.model_dump(exclude_none=True, by_alias=True),
            **kwargs)

        return response

    def put_v1_account_password(self, change_password: ChangePassword, **kwargs) -> Response:
        """
        Change registered user password
        :param
        :return:
        """
        response = self.put(
            path=f'/v1/account/password',
            json=change_password.model_dump(exclude_none=True, by_alias=True),
            **kwargs
        )
        return response

    def get_v1_account(self, **kwargs) -> Response:
        """
        Get current user
        """
        response = self.get(
            path='/v1/account',
            **kwargs
        )

        return response

    def put_v1_account_token(self, token: str) -> Response:
        headers = {'accept': 'application/json'}

        response = self.put(
            path=f'/v1/account/{token}',
            headers=headers
        )

        return response

    def post_v1_account_password(self, reset_password: ResetPassword, **kwargs) -> Response:
        """
        Reset registered user password
        :param
        :return:
        """
        response = self.post(
            path=f'/v1/account/password',
            json=reset_password.model_dump(exclude_none=True, by_alias=True),
            **kwargs
        )

        return response

    def put_v1_account_mail(self, change_mail: ChangeEmail, **kwargs) -> Response:
        """
        Change registered user email
        :param json_data:
        :return:
        """
        headers = {
            'accept': 'text/plain',
            'Content-Type': 'application/json'
        }
        response = self.put(
            path=f'/v1/account/email',
            headers=headers,
            json=change_mail.model_dump(exclude_none=True, by_alias=True),
            **kwargs
        )

        return response

    def post_v1_account_login(self, login_credentials: LoginCredentials, **kwargs) -> Response:
        response = self.post(
            path="/v1/account/login",
            json=login_credentials.model_dump(exclude_none=True, by_alias=True),
            **kwargs
        )
        return response
