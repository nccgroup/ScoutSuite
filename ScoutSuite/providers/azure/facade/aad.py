from azure.graphrbac import GraphRbacManagementClient

import requests
import uuid

from ScoutSuite.core.console import print_exception
from ScoutSuite.providers.utils import run_concurrently


class AADFacade:
    def __init__(self, credentials):
        self._client = GraphRbacManagementClient(credentials.aad_graph_credentials,
                                                 tenant_id=credentials.get_tenant_id())

        self._microsoft_graph_session = requests.Session()
        self._microsoft_graph_session.headers.update(
            {'Authorization': 'Bearer {}'.format(credentials.microsoft_graph_credentials.token['access_token']),
             'User-Agent': 'scout-suite',
             'Accept': 'application/json',
             'Content-Type': 'application/json',
             'SdkVersion': 'scout-suite',
             'return-client-request-id': 'true'})

    async def _get_microsoft_graph_response(self, api_resource, api_version='v1.0'):
        endpoint = 'https://graph.microsoft.com/{}/{}'.format(api_version, api_resource)
        http_headers = {'client-request-id': str(uuid.uuid4())}
        try:
            response = self._microsoft_graph_session.get(endpoint, headers=http_headers, stream=False)
            if response.status_code == 200:
                return response.json()
            else:
                print_exception('Failed to query Microsoft Graph endpoint \"{}\": status code {}'.
                                format(api_resource, response.status_code))
        except Exception as e:
            print_exception('Failed to query Microsoft Graph endpoint \"{}\": {}'.format(api_resource, e))
            return {}

    async def get_users(self):
        try:
            return await run_concurrently(lambda: list(self._client.users.list()))
        except Exception as e:
            print_exception('Failed to retrieve users: {}'.format(e))
            return []

    async def get_groups(self):
        try:
            return await run_concurrently(lambda: list(self._client.groups.list()))
        except Exception as e:
            print_exception('Failed to retrieve groups: {}'.format(e))
            return []

    async def get_group_details(self, group_id):
        response = await self._get_microsoft_graph_response('groups/{}'.format(group_id))
        return response

    async def get_user_groups(self, user_id):
        try:
            return await run_concurrently(lambda: list(
                self._client.users.get_member_groups(object_id=user_id,
                                                     security_enabled_only=False))
                                          )
        except Exception as e:
            print_exception('Failed to retrieve user\'s groups: {}'.format(e))
            return []

    async def get_service_principals(self):
        try:
            return await run_concurrently(lambda: list(self._client.service_principals.list()))
        except Exception as e:
            print_exception('Failed to retrieve service principals: {}'.format(e))
            return []

    async def get_applications(self):
        try:
            return await run_concurrently(lambda: list(self._client.applications.list()))
        except Exception as e:
            print_exception('Failed to retrieve applications: {}'.format(e))
            return []
