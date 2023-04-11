import json
import requests

from ksyun.common.common_client import CommonClient
from ksyun.common import credential
from ksyun.common.exception.ksyun_sdk_exception import KsyunSDKException
from ksyun.common.profile.client_profile import ClientProfile
from ksyun.common.profile.http_profile import HttpProfile

from ScoutSuite.providers.base.authentication_strategy import AuthenticationStrategy, AuthenticationException


class KsyunCredentials:

    def __init__(self, credentials_id, credentials_secret, credentials_cookie, account_id, project_list):
        self.credentials_id = credentials_id
        self.credentials_secret = credentials_secret
        self.credentials_cookie = credentials_cookie
        self.account_id = account_id
        self.project_list = project_list


class KsyunAuthenticationStrategy(AuthenticationStrategy):
    """
    Implements authentication for the Kingsoft Cloud provider
    """

    def authenticate(self, access_key_id=None, access_key_secret=None, access_key_cookie=None, **kwargs):

        try:
            access_key_id = access_key_id if access_key_id else input('Access Key ID:')
            access_key_secret = access_key_secret if access_key_secret else input('Secret Access Key:')
            access_key_cookie = access_key_cookie if access_key_cookie else input('Cookie Key Value:')
            account_id = self.get_user(access_key_cookie)
            project_list = self.GetAccountAllProjectList(access_key_id, access_key_secret)
            return KsyunCredentials(access_key_id, access_key_secret, access_key_cookie, account_id, project_list)

        except Exception as e:
            raise AuthenticationException(e)

    def get_user(self, access_key_cookie):
        url = "https://account.console.ksyun.com/i/console/user/get_user"
        headers = {
            "Accept": "application/json",
            "Cookie": access_key_cookie
        }
        r = requests.get(url, headers=headers)
        account_id = json.loads(r.text).get("data").get("user").get("id")
        if account_id:
            return account_id
        else:
            return None

    def GetAccountAllProjectList(self, access_key_id, access_key_secret):
        try:
            projects = []
            cred = credential.Credential(access_key_id, access_key_secret)

            httpProfile = HttpProfile()
            httpProfile.endpoint = "iam.api.ksyun.com"
            httpProfile.reqMethod = "POST"
            httpProfile.reqTimeout = 60
            httpProfile.scheme = "http"

            clientProfile = ClientProfile()
            clientProfile.httpProfile = httpProfile

            common_client = CommonClient("iam", '2015-11-01', cred, "cn-beijing-6", profile=clientProfile)
            r = common_client.call("GetAccountAllProjectList", {})
            items = json.loads(r).get('ListProjectResult').get('ProjectList')
            if items:
                for item in items:
                    projects.append(item['ProjectId'])
                return projects
            else:
                return []
        except KsyunSDKException as err:
            print(err)