import json
import requests
from ksyun.common.common_client import CommonClient
from ksyun.common import credential
from ksyun.common.exception.ksyun_sdk_exception import KsyunSDKException
from ksyun.common.profile.client_profile import ClientProfile
from ksyun.common.profile.http_profile import HttpProfile

from ScoutSuite.providers.ksyun.authentication_strategy import KsyunCredentials


class RAMFacade():
    def __init__(self, credentials: KsyunCredentials):
        self._credentials = credentials
        cred = credential.Credential(self._credentials.credentials_id, self._credentials.credentials_secret)
        httpProfile = HttpProfile()
        httpProfile.endpoint = "iam.api.ksyun.com"
        httpProfile.reqMethod = "POST"
        httpProfile.reqTimeout = 60
        httpProfile.scheme = "http"

        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile

        self.common_client = CommonClient("iam", '2015-11-01', cred, "cn-beijing-6", profile=clientProfile)

    async def get_users(self):
        """
        Get all users

        :return: a list of all users
        """
        # response = await get_response(client=self._client, request=ListUsersRequest.ListUsersRequest())
        try:
            r = self.common_client.call("ListUsers", {})
            response = json.loads(r).get('ListUserResult')
            if response:
                return response['Users']['member']
            else:
                return []
        except KsyunSDKException as err:
            print(err)

    async def get_user_details(self, username):
        """
        Get additional details for a user

        :param username: The username of the user
        :return: a dict with the user's details
        """
        try:
            r = self.common_client.call("GetUser", {"UserName": username})
            response = json.loads(r).get("GetUserResult")
            if response:
                return response['User']
            else:
                return []
        except KsyunSDKException as err:
            print(err)

    async def get_user_mfa_status(self, username):

        try:
            r = self.common_client.call("GetVirtualMFADevice", {"UserName": username})
            response = json.loads(r).get("VirtualMFADevice")
            if response:
                return response['SerialNumber']
            else:
                return None
        except KsyunSDKException as err:
            print(err)
            return None

    async def get_user_api_keys(self, username):
        """
        Get API keys for a user

        :param username: The username of the user
        :return: the list of API keys for that user
        """
        try:
            r = self.common_client.call("ListAccessKeys", {"UserName": username})
            response = json.loads(r).get('ListAccessKeyResult')
            if response:
                return response['AccessKeyMetadata']['member']
            else:
                return []
        except KsyunSDKException as err:
            print(err)
            return []

    async def get_groups(self):
        """
        Get all groups

        :return: a list of all groups
        """
        try:
            r = self.common_client.call("ListGroups", {})
            response = json.loads(r).get('ListGroupsResult')
            if response:
                return response['Groups']['member']
            else:
                return []
        except KsyunSDKException as err:
            print(err)
            return []

    async def get_group_users(self, group_name):
        """
        Get all users in a group

        :return: a list of users in groups
        """
        try:
            r = self.common_client.call("listUsersForGroup", {"GroupName": group_name})
            response = json.loads(r).get('GetGroupResult')

            if response:
                return response['Group']['Group']
            else:
                return []
        except KsyunSDKException as err:
            print(err)
            return []

    async def get_policies(self):
        """
        Get all custom policies

        :return: a list of all custom policies
        """
        try:
            r = self.common_client.call("ListPolicies", {})
            response = json.loads(r).get('ListPoliciesResult')

            if response:
                return response['Policies']['member']
            else:
                return []
        except KsyunSDKException as err:
            print(err)
            return []

    async def get_policy_version(self, krn, version):
        """
        Get all policies

        :return: a list of all policies
        """
        try:
            r = self.common_client.call("GetPolicyVersion", {"PolicyKrn": krn, "VersionId": version})
            response = json.loads(r).get('GetPolicyVersionResult')
            if response:
                return response['PolicyVersion']
            else:
                return []
        except KsyunSDKException as err:
            print(err)
            return []

    async def get_policy_entities(self, krn):
        """
        Get all entities for a policy

        :return: a dict of all policy entities
        """
        try:
            r = self.common_client.call("ListEntitiesForPolicy", {"PolicyKrn": krn})
            response = json.loads(r).get('ListEntitiesForPolicyResult')
            if response:
                return response
            else:
                return []
        except KsyunSDKException as err:
            print(err)
            return []

    async def get_roles(self):
        """
        Get all roles

        :return: a list of all roles
        """
        try:
            r = self.common_client.call("ListRoles", {})
            response = json.loads(r).get('ListRolesResult')
            if response:
                return response['Roles']['member']
            else:
                return []
        except KsyunSDKException as err:
            print(err)
            return []

    async def get_password_policy(self):
        url = "https://uc.console.ksyun.com/i/console/iam/user/getPwdPolicy"
        headers = {
            "Accept": "application/json",
            "Cookie": "kscdigest=77372c6d8a01ef3b46dca11e3ef3f1dc-1344489989;"
        }
        try:
            r = requests.get(url, headers=headers)
            response = json.loads(r.text).get("data")
            if response:
                return response
            else:
                return []
        except KsyunSDKException as err:
            return []

    async def get_security_policy(self):
        pass