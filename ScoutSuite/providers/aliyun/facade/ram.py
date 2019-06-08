from ScoutSuite.providers.aliyun.authentication_strategy import AliyunCredentials
from ScoutSuite.providers.aliyun.facade.utils import get_response

from ScoutSuite.core.console import print_exception
from aliyunsdkram.request.v20150501 import ListUsersRequest, ListAccessKeysRequest, \
    GetUserMFAInfoRequest, GetUserRequest, GetAccessKeyLastUsedRequest, GetPasswordPolicyRequest, \
    GetSecurityPreferenceRequest


class RAMFacade:
    def __init__(self, credentials: AliyunCredentials):
        self._client = credentials.client

    async def get_users(self):
        """
        Get all users

        :return: a list of all users
        """
        response = await get_response(client=self._client,
                                request=ListUsersRequest.ListUsersRequest())
        return response['Users']['User']


    async def get_user_details(self, username):
        """
        Get additional details for a user

        :param username: The username of the user
        :return: a dict with the user's details
        """
        request = GetUserRequest.GetUserRequest()
        request.set_UserName(username)
        response = await get_response(client=self._client,
                                      request=request)
        return response['User']

    async def get_user_api_keys(self, username):
        """
        Get API keys for a user

        :param username: The username of the user
        :return: the list of API keys for that user
        """
        request = ListAccessKeysRequest.ListAccessKeysRequest()
        request.set_UserName(username)
        response = await get_response(client=self._client,
                                      request=request)
        return response['AccessKeys']['AccessKey']

    async def get_user_api_key_last_usage(self, username, key_id):
        """
        Get last usage date for an API key

        :param username: The username of the user
        :param key_id: The API key id
        :return: the list of API keys for that user
        """
        request = GetAccessKeyLastUsedRequest.GetAccessKeyLastUsedRequest()
        request.set_UserName(username)
        request.set_UserAccessKeyId(key_id)
        response = await get_response(client=self._client,
                                      request=request)
        return response['AccessKeyLastUsed']['LastUsedDate']

    async def get_user_mfa_status(self, username):
        """
        Check if user has MFA configured

        :param username: The username of the user
        :return: status and MFA serial number
        """
        request = GetUserMFAInfoRequest.GetUserMFAInfoRequest()
        request.set_UserName(username)
        try:
            response = await get_response(client=self._client,
                                          request=request)
        except Exception as e:
            # TODO can't seem to differenciate between a user that has MFA disabled
            # and a user that has MFA enabled but not configured
            if e.error_code == 'EntityNotExist.User.MFADevice':
                # ignore, MFA is not configured
                return False, None
            else:
                print_exception('Unable to get MFA status for user {}: {}'.format(username,
                                                                                  e))
                return False, None
        else:
            return True, response['MFADevice']['SerialNumber']

    async def get_password_policy(self):
        """
        Get the account's password policy

        :return: the password policy
        """
        request = GetPasswordPolicyRequest.GetPasswordPolicyRequest()
        response = await get_response(client=self._client,
                                      request=request)
        return response['PasswordPolicy']

    async def get_security_policy(self):
        """
        Get the account's security policy

        :return: the security policy
        """
        request = GetSecurityPreferenceRequest.GetSecurityPreferenceRequest()
        response = await get_response(client=self._client,
                                      request=request)
        return response['SecurityPreference']
