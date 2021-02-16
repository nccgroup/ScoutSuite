from ScoutSuite.providers.aliyun.resources.base import AliyunResources
from ScoutSuite.providers.aliyun.facade.base import AliyunFacade
from ScoutSuite.core.console import print_exception
import json


class Policies(AliyunResources):
    def __init__(self, facade: AliyunFacade):
        super().__init__(facade)

    async def fetch_all(self):
        parsing_error_counter = 0
        for raw_policy in await self.facade.ram.get_policies():
            try:
                id, policy = await self._parse_policy(raw_policy)
                if id:
                    self[id] = policy
            except Exception as e:
                parsing_error_counter += 1
        if parsing_error_counter > 0:
            print_exception(
                'Failed to parse {} resource: {} times'.format(self.__class__.__name__, parsing_error_counter))

    async def _parse_policy(self, raw_policy):
        """
        Only processing policies with an
        :param raw_policy:
        :return:
        """
        if raw_policy.get('AttachmentCount') > 0:
            policy_dict = {}
            policy_dict['id'] = policy_dict['name'] = raw_policy.get('PolicyName')
            policy_dict['description'] = raw_policy.get('Description')
            policy_dict['create_date'] = raw_policy.get('CreateDate')
            policy_dict['update_date'] = raw_policy.get('UpdateDate')
            policy_dict['attachment_count'] = raw_policy.get('AttachmentCount')
            policy_dict['type'] = raw_policy.get('PolicyType')
            policy_dict['default_version'] = raw_policy.get('DefaultVersion')

            policy_version = await self.facade.ram.get_policy_version(policy_dict['name'],
                                                                      policy_dict['type'],
                                                                      policy_dict['default_version'])
            policy_version['PolicyDocument'] = json.loads(policy_version['PolicyDocument'])
            # policy_dict['policy_document'] = policy_version['PolicyDocument']
            policy_dict['policy_document'] = policy_version

            policy_entities = await self.facade.ram.get_policy_entities(policy_dict['name'],
                                                                      policy_dict['type'])
            policy_dict['entities'] = {}
            if policy_entities['Users']['User']:
                policy_dict['entities']['users'] = []
                for user in policy_entities['Users']['User']:
                    policy_dict['entities']['users'].append(user['UserName'])
            if policy_entities['Groups']['Group']:
                policy_dict['entities']['groups'] = []
                for group in policy_entities['Groups']['Group']:
                    policy_dict['entities']['groups'].append(group['GroupName'])
            if policy_entities['Roles']['Role']:
                policy_dict['entities']['roles'] = []
                for role in policy_entities['Roles']['Role']:
                    policy_dict['entities']['roles'].append(role['RoleName'])

            return policy_dict['id'], policy_dict
        else:
            return None, None
