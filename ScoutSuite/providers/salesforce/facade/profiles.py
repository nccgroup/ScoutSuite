import requests
import json

from ScoutSuite.providers.salesforce.authentication_strategy import SalesforceCredentials
from ScoutSuite.core.console import print_exception


class ProfileFacade:
    def __init__(self, credentials: SalesforceCredentials):
        self._credentials = credentials

    async def get_profiles(self):
        try:

            rest_headers = {'Authorization': 'Bearer ' + self._credentials.session_id}

            try:
                response = requests.get('https://{}/services/data/v48.0/query/?q='
                                        'SELECT+Id,Name,PermissionsApiEnabled,PermissionsApexRestServices+from+Profile'.
                                        format(self._credentials.endpoint),
                                        headers=rest_headers)
            except Exception as e:
                print_exception('Failed to get profiles: {}'.format(e))
                return []

            try:
                profile_json = json.loads(response.text)['records']
            except Exception as e:
                print_exception('Failed to parse profiles: {}'.format(e))
            else:
                return profile_json

        except Exception as e:
            print_exception('Failed to get profiles: {}'.format(e))
            return []
