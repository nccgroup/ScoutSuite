import json

from msgraphcore import GraphSession
from ScoutSuite.core.console import print_exception


class MicrosoftGraphFacade:

    def __init__(self, credentials):
        self.credentials = credentials

    async def _get_microsoft_graph_response(self, api_resource, api_version='v1.0'):
        scopes = ['https://graph.microsoft.com/.default']
        cli = GraphSession(self.credentials.get_credentials('aad_graph'), scopes)
        endpoint = 'https://graph.microsoft.com/{}/{}'.format(api_version, api_resource)
        try:
            response = cli.get(endpoint )
            if response.status_code == 200:
                return response.json()
            else:
                print_exception('Failed to query Microsoft Graph endpoint \"{}\": status code {}'.
                                format(api_resource, response.status_code))
                return {}
        except Exception as e:
            print_exception('Failed to query Microsoft Graph endpoint \"{}\": {}'.format(api_resource, e))
            return {}

    async def get_microsoft_graph_users(self):
        try:
            test = await self._get_microsoft_graph_response('users')
            test_beta = await self._get_microsoft_graph_response('users', 'beta')
            if not test_beta:
                users = test_beta.get('value')
                users_filtered = [d for d in users if d['userType'] in 'Guest']
                return users_filtered
            else:
                return test_beta
        except Exception as e:
            print_exception(f'Failed to retrieve users: {e}')
            return []

    async def get_microsoft_graph_user(self, user_id):
        try:
            test = await self._get_microsoft_graph_response('users/{}'.format(user_id))
            test_beta = await self._get_microsoft_graph_response('users/{}'.format(user_id), 'beta')
            return test_beta
        except Exception as e:
            print_exception(f'Failed to retrieve user {user_id}: {e}')
            return None

    async def get_microsoft_graph_groups(self):
        try:
            test = await self._get_microsoft_graph_response('groups')
            test_beta = await self._get_microsoft_graph_response('groups', 'beta')
            if not test_beta:
                groups = test_beta.get('value')
                return groups
            else:
                return test_beta
        except Exception as e:
            print_exception(f'Failed to retrieve groups: {e}')
            return []

    async def get_microsoft_graph_user_groups(self, group_id):
        try:
            test = await self._get_microsoft_graph_response('groups/{}'.format(group_id))
            test_beta = await self._get_microsoft_graph_response('groups/{}'.format(group_id), 'beta')
            groups = test_beta.get('value')
            return groups
        except Exception as e:
            print_exception(f'Failed to retrieve user\'s groups: {e}')
            return []

    async def get_microsoft_graph_service_principals(self):
        try:
            test = await self._get_microsoft_graph_response('servicePrincipals')
            test_beta = await self._get_microsoft_graph_response('servicePrincipals', 'beta')
            if not test_beta:
                service_principals = test_beta.get('value')
                return service_principals
            else:
                return test_beta
        except Exception as e:
            print_exception(f'Failed to retrieve service principals: {e}')
            return []

    async def get_microsoft_graph_applications(self):
        try:
            test = await self._get_microsoft_graph_response('applications')
            test_beta = await self._get_microsoft_graph_response('applications', 'beta')
            if not test_beta:
                applications = test_beta.get('value')
                return applications
            else:
                return test_beta
        except Exception as e:
            print_exception(f'Failed to retrieve applications: {e}')
            return []

