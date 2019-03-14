from ScoutSuite.providers.aws.resources.resources import AWSResources


class Policies(AWSResources):
    async def fetch_all(self, **kwargs):
        raw_policies = await self.facade.iam.get_policies()
        for raw_policy in raw_policies:
            name, resource = self._parse_policy(raw_policy)
            self[name] = resource

    def _parse_policy(self, raw_policy):
        raw_policy['id'] = raw_policy.pop('PolicyId')
        raw_policy['name'] = raw_policy.pop('PolicyName')
        raw_policy['arn'] = raw_policy.pop('Arn')
        return raw_policy['id'], raw_policy
