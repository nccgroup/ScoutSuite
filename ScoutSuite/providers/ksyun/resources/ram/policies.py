from ScoutSuite.providers.ksyun.resources.base import KsyunResources
from ScoutSuite.providers.ksyun.facade.base import KsyunFacade
import json


class Policies(KsyunResources):
    def __init__(self, facade: KsyunFacade):
        super().__init__(facade)

    async def fetch_all(self):
        for raw_policy in await self.facade.ram.get_policies():
            id, policy = await self._parse_policy(raw_policy)
            if id:
                self[id] = policy

    async def _parse_policy(self, raw_policy):
        if raw_policy.get('AttachmentCount') > 0:
            policy_dict = {}
            policy_dict['id'] = raw_policy.get('PolicyId')
            policy_dict['krn'] = raw_policy.get('Krn')
            policy_dict['name'] = raw_policy.get('PolicyName')
            policy_dict['service_id'] = raw_policy.get('ServiceId')
            policy_dict['service_name'] = raw_policy.get('ServiceName')
            policy_dict['service_view_name'] = raw_policy.get('ServiceViewName')
            policy_dict['description'] = raw_policy.get('Description')
            policy_dict['create_date'] = raw_policy.get('CreateDate')
            policy_dict['update_date'] = raw_policy.get('UpdateDate')
            policy_dict['attachment_count'] = raw_policy.get('AttachmentCount')
            policy_dict['policy_type'] = raw_policy.get('PolicyType')
            policy_dict['default_version_id'] = raw_policy.get('DefaultVersionId')

            policy_version = await self.facade.ram.get_policy_version(policy_dict['krn'], policy_dict['default_version_id'])
            policy_dict['policy_document'] = policy_version['Document']

            policy_entities = await self.facade.ram.get_policy_entities(policy_dict['krn'])
            policy_dict['entities'] = {}
            if policy_entities['PolicyUsers']['member']:
                policy_dict['entities']['users'] = []
                for user in policy_entities['PolicyUsers']['member']:
                    policy_dict['entities']['users'].append(user['UserName'])
            if policy_entities['PolicyGroups']['member']:
                policy_dict['entities']['groups'] = []
                for group in policy_entities['PolicyGroups']['member']:
                    policy_dict['entities']['groups'].append(group['GroupName'])
            if policy_entities['PolicyRoles']['member']:
                policy_dict['entities']['roles'] = []
                for role in policy_entities['PolicyRoles']['member']:
                    policy_dict['entities']['roles'].append(role['RoleName'])

            return policy_dict['id'], policy_dict
        else:
            return None, None
