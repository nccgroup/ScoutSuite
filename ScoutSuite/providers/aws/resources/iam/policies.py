from ScoutSuite.providers.aws.resources.base import AWSResources
from ScoutSuite.core.console import print_exception


class Policies(AWSResources):
    async def fetch_all(self):
        raw_policies = await self.facade.iam.get_policies()
        parsing_error_counter = 0
        for raw_policy in raw_policies:
            try:
                name, resource = self._parse_policy(raw_policy)
                self[name] = resource
            except Exception as e:
                parsing_error_counter += 1
        if parsing_error_counter > 0:
            print_exception(
                'Failed to parse {} resource: {} times'.format(self.__class__.__name__, parsing_error_counter))

    def _parse_policy(self, raw_policy):
        policy = {}
        policy['id'] = raw_policy.pop('PolicyId')
        policy['name'] = raw_policy.pop('PolicyName')
        policy['arn'] = raw_policy.pop('Arn')
        policy['PolicyDocument'] = raw_policy.pop('PolicyDocument')
        policy['attached_to'] = raw_policy.pop('attached_to')

        return policy['id'], policy
