from msgraph.core import GraphClient

from ScoutSuite.core.console import print_exception


class AADFacade:

    def __init__(self, credentials):
        self.credentials = credentials


    async def _get_microsoft_graph_response(self, api_resource, api_version='v1.0'):
        scopes = ['https://graph.microsoft.com/.default']

        client = GraphClient(credential=self.credentials.get_credentials(), scopes=scopes)
        endpoint = 'https://graph.microsoft.com/{}/{}'.format(api_version, api_resource)
        try:
            response = client.get(endpoint)
            if response.status_code == 200:
                return response.json()
            # If response is 404 then it means there is no resource associated with the provided id
            elif response.status_code == 404:
                return {}
            else:
                print_exception('Failed to query Microsoft Graph endpoint \"{}\": status code {}'.
                                format(api_resource, response.status_code))
                return {}
        except Exception as e:
            print_exception('Failed to query Microsoft Graph endpoint \"{}\": {}'.format(api_resource, e))
            return {}

    async def get_users(self):
        try:
            # This filters down the users which are pulled from the directory, otherwise for large tenants this
            # becomes out of hands
            # See https://github.com/nccgroup/ScoutSuite/issues/698
            user_filter = '?$filter=userType+eq+%27Guest%27'
            users_response_beta = await self._get_microsoft_graph_response('users'+ user_filter, 'beta')
            if users_response_beta:
                users = users_response_beta.get('value')
                return users
            return users_response_beta
        except Exception as e:
            print_exception(f'Failed to retrieve users: {e}')
            return []

    async def get_user(self, user_id):
        try:
            user_filter = f'?$filter=id+eq+%27{user_id}%27'
            user_response_beta = await self._get_microsoft_graph_response('users'+user_filter, 'beta')
            if user_response_beta:
                users = user_response_beta.get('value')
                return users[0]
            return user_response_beta
        except Exception as e:
            print_exception(f'Failed to retrieve user {user_id}: {e}')
            return None

    async def get_groups(self):
        try:
            groups_response = await self._get_microsoft_graph_response('groups')
            if groups_response:
                groups = groups_response.get('value')
                return groups
            return groups_response
        except Exception as e:
            print_exception(f'Failed to retrieve groups: {e}')
            return []

    async def get_user_groups(self, group_id):
        try:
            group_filter = f'?$filter=id+eq+%27{group_id}%27'
            user_groups_response = await self._get_microsoft_graph_response('groups' + group_filter)
            if user_groups_response:
                groups = user_groups_response.get('value')
                return groups
            return user_groups_response
        except Exception as e:
            print_exception(f'Failed to retrieve user\'s groups: {e}')
            return []

    async def get_service_principals(self):
        try:
            # Need publisher name value for serviceprincipals.py. v1.0 does not have that value, thus we use beta
            service_principals_response_beta = await self._get_microsoft_graph_response('servicePrincipals', 'beta')
            if service_principals_response_beta:
                service_principals = service_principals_response_beta.get('value')
                return service_principals
            return service_principals_response_beta
        except Exception as e:
            print_exception(f'Failed to retrieve service principals: {e}')
            return []

    async def get_applications(self):
        try:
            applications_response = await self._get_microsoft_graph_response('applications')
            if applications_response:
                applications = applications_response.get('value')
                return applications
            return applications_response
        except Exception as e:
            print_exception(f'Failed to retrieve applications: {e}')
            return []

    async def get_policies(self):
        try:
            policies_response = await self._get_microsoft_graph_response('policies/authorizationPolicy')
            return policies_response
        except Exception as e:
            print_exception(f'Failed to retrieve policies: {e}')
            return []
