from dm_api_account.models.change_email import ChangeEmail
from dm_api_account.models.registration import Registration
from dm_api_account.models.user_details_envelope import UserDetailsEnvelope
from restclient.client import RestClient


class AccountApi(RestClient):

    def post_v1_account(self, registration: Registration):
        """
        Register new user
        :param json_data:
        :return:
        """
        response = self.post(
            path=f'/v1/account',
            json=registration.model_dump(exclude_none=True, by_alias=True)
        )
        return response

    def post_v1_account_password(self, **kwargs):
        """
        Reset registered user password
        :param
        :return:
        """
        response = self.post(
            path=f'/v1/account/password',
            **kwargs)

        return response

    def put_v1_account_password(self, **kwargs):
        """
        Change registered user password
        :param
        :return:
        """
        response = self.put(
            path=f'/v1/account/password',
            **kwargs
        )
        return response

    def get_v1_account(self, **kwargs):
        """
        Get current user
        """
        response = self.get(
            path='/v1/account',
            **kwargs
        )

        return response

    def get_v1_account_dto(self, **kwargs):
        """
        Get current user as DTO
        """
        response = self.get_v1_account(**kwargs)

        return UserDetailsEnvelope.model_validate(response.json())

    def put_v1_account_token(self, token: str):
        headers = {'accept': 'application/json'}

        response = self.put(
            path=f'/v1/account/{token}',
            headers=headers
        )

        return response

    def put_v1_account_mail(self, change_mail: ChangeEmail):
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
            json=change_mail.model_dump(exclude_none=True, by_alias=True)
        )
        return response

    def post_v1_account_login(self, login: str, password: str):
        response = self.post(
            path="/v1/account/login",
            json={
                "login": login,
                "password": password,
                "rememberMe": True
            }
        )
        return response
