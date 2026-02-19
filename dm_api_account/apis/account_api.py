import requests

from dm_api_account.models.change_email import ChangeEmail
from dm_api_account.models.registration import Registration
from dm_api_account.models.user_details_envelope import UserDetailsEnvelope
from dm_api_account.models.user_envelope import UserEnvelope
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

    def post_v1_account_reset_password(self, json_data):
        """
        Reset registered user password
        :param json_data:
        :return:
        """
        response = self.post(
            path=f'/v1/account/password',
            json=json_data
        )
        return response

    def put_v1_account_change_password(self, json_data):
        """
        Change registered user password
        :param json_data:
        :return:
        """
        response = self.put(
            path=f'/v1/account/password',
            json=json_data
        )
        return response

    # def get_v1_account(self, **kwargs):
    #     """
    #     Get current user
    #     :return:
    #     """
    #     response = self.get(
    #         path=f'/v1/account',
    #         **kwargs
    #     )
    #     return response

    def get_v1_account(self, **kwargs):
        """
        Get current user (raw response)
        """
        return self.get(
            path='/v1/account',
            **kwargs
        )

    def get_v1_account_dto(self, **kwargs) -> UserDetailsEnvelope:
        """
        Get current user as DTO
        """
        response = self.get_v1_account(**kwargs)

        return UserDetailsEnvelope.model_validate(response.json())

    def put_v1_account_token(self, token, validate_response=True):
        """
        Activate registered user
        :param token:
        :return:
        """
        headers = {
            'accept': 'text/plain',
        }
        response = self.put(
            path=f'/v1/account/{token}',
            headers=headers
        )
        if validate_response:
            return UserEnvelope(**response.json())
        return response

    def put_v1_account_change_mail(self, change_mail: ChangeEmail):
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
