# -*- coding: utf-8 -*-

from ScoutSuite.providers.gcp.configs.base import GCPBaseConfig

from opinel.utils.console import printError, printException, printInfo

from googleapiclient import discovery
from ScoutSuite.providers.gcp.utils import gcp_connect_service


class IAMConfig(GCPBaseConfig):
    targets = (
        ('projects.serviceAccounts', 'Service Accounts', 'list', {'name': 'projects/{{project_placeholder}}'}, False),
    )

    def __init__(self, thread_config):

        self.library_type = 'api_client_library'

        self.service_accounts = {}
        self.service_accounts_count = 0

        super(IAMConfig, self).__init__(thread_config)

    def parse_projects_serviceAccounts(self, service_account, params):

        service_account_dict = {}

        service_account_dict['id'] = service_account['uniqueId']
        service_account_dict['display_name'] = service_account['displayName'] if 'displayName' in service_account else 'N/A'
        service_account_dict['name'] = service_account['email']
        service_account_dict['email'] = service_account['email']
        service_account_dict['project_id'] = service_account['projectId']

        keys = self._get_service_account_keys(params['api_client'],
                                              service_account_dict['project_id'],
                                              service_account_dict['email'])
        service_account_dict['keys'] = {}
        if keys:
            for key in keys:
                service_account_dict['keys'][key['name'].split('/')[-1]] = {
                    'valid_after': key['validAfterTime'],
                    'valid_before': key['validBeforeTime'],
                    'key_algorithm': key['keyAlgorithm']
                }

        bindings = self._get_service_account_iam_policy(params['api_client'],
                                                        service_account_dict['project_id'],
                                                        service_account_dict['email'])
        service_account_dict['bindings'] = []
        if bindings:
            service_account_dict['bindings'] = bindings


        self.service_accounts[service_account_dict['id']] = service_account_dict

        # required as target is 'projects.serviceAccounts' and not 'service_accounts'
        self.service_accounts_count+=1


    def _get_service_account_keys(self, api_client, project_id, service_account_email):

        try:
            #FIXME for some reason using the api_client fails, creating a new client doesn't generate an error...
            client = discovery.build('iam', 'v1', cache_discovery=False)
            # client = gcp_connect_service(service='iam')

            # response = api_client.projects().serviceAccounts().keys().list(
            response = client.projects().serviceAccounts().keys().list(
                name='projects/%s/serviceAccounts/%s' % (project_id, service_account_email)).execute()
            if 'keys' in response:
                return response['keys']
            else:
                return None
        except Exception as e:
            printError('Failed to get keys for service account %s: %s' % (service_account_email, e))
            return None

    def _get_service_account_iam_policy(self, api_client, project_id, service_account_email):

        try:
            #FIXME for some reason using the api_client fails, creating a new client doesn't generate an error...
            client = discovery.build('iam', 'v1')

            # response = api_client.projects().serviceAccounts().getIamPolicy(
            response = client.projects().serviceAccounts().getIamPolicy(
                resource='projects/%s/serviceAccounts/%s' % (project_id, service_account_email)).execute()
            if 'bindings' in response:
                return response['bindings']
            else:
                return None
        except Exception as e:
            printError('Failed to get IAM policy for service account %s: %s' % (service_account_email, e))
            return None
