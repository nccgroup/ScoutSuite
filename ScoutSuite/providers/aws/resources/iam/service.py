import asyncio

from ScoutSuite.providers.aws.resources.resources import AWSCompositeResources
from ScoutSuite.providers.aws.resources.iam.credentialreports import CredentialReports
from ScoutSuite.providers.aws.resources.iam.groups import Groups
from ScoutSuite.providers.aws.resources.iam.policies import Policies
from ScoutSuite.providers.aws.resources.iam.users import Users
from ScoutSuite.providers.aws.facade.facade import AWSFacade


class IAM(AWSCompositeResources):
    _children = [
        (CredentialReports, 'credential_reports'),
        (Groups, 'groups'),
        (Policies, 'policies'),
        (Users, 'users')
    ]

    def __init__(self):
        # TODO: Should be injected
        self.facade = AWSFacade()
        self.service = 'iam'

    async def fetch_all(self, credentials, regions=None, partition_name='aws'):
        # TODO: This should not be set here, the facade should be injected and already authenticated
        self.facade._set_session(credentials)
        await self._fetch_children(self, {})

    def finalize(self):
        # Update permissions for managed policies
        for policy in self['policies'].values():
            if 'attached_to' in policy and len(policy['attached_to']) > 0:
                for entity_type in policy['attached_to']:
                    for entity in policy['attached_to'][entity_type]:
                        entity['id'] = self.get_id_for_resource(entity_type, entity['name'])
                        entities = self[entity_type] 
                        entities[entity['id']]['policies'] = [] # TODO : if does not exist
                        entities[entity['id']]['policies_counts'] = 0 # TODO : if does not exist
                        entities[entity['id']]['policies'].append(policy['id'])
                        entities[entity['id']]['policies_counts'] += 1
                # self.__parse_permissions(policy_id, policy['PolicyDocument'], 'policies',
                #                          entity_type, entity['id'])
            else:
                pass
                # self.__parse_permissions(policy_id, self.policies[policy_id]['PolicyDocument'], 'policies', None, None)

    def get_id_for_resource(self, iam_resource_type, resource_name):
        for resource_id in self[iam_resource_type]:
            if self[iam_resource_type][resource_id]['name'] == resource_name:
                return resource_id
