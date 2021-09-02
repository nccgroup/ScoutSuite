from ScoutSuite.providers.aws.resources.base import AWSResources


class Policies(AWSResources):
    async def fetch_all(self):
        raw_policies = await self.facade.iam.get_policies()
        for raw_policy in raw_policies:
            name, resource = self._parse_policy(raw_policy)
            self[name] = resource

    def _parse_policy(self, raw_policy):
        policy = {}
        policy['id'] = raw_policy.pop('PolicyId')
        policy['name'] = raw_policy.pop('PolicyName')
        policy['arn'] = raw_policy.pop('Arn')
        policy['PolicyDocument'] = raw_policy.pop('PolicyDocument')
        policy['attached_to'] = raw_policy.pop('attached_to')
        policy['management'] = 'AWS' if policy['arn'].startswith(f"arn:{self.facade.partition}:iam::aws:") else 'Customer'

        return policy['id'], policy
