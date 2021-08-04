from ScoutSuite.providers.aws.resources.base import AWSResources


class ServicePolicies(AWSResources):
    async def fetch_all(self):
        raw_policies = await self.facade.organizations.get_service_policies()
        for raw_policy in raw_policies:
            name, resource = self._parse_policy(raw_policy)
            self[name] = resource

    def _parse_policy(self, raw_policy):
        policy = {}
        policy["id"] = raw_policy.get("Id")
        policy["name"] = raw_policy.get("Name")
        policy["arn"] = raw_policy.get("Arn")
        policy["description"] = raw_policy.get("Description")
        policy["type"] = raw_policy.get("Type")
        policy["aws_managed"] = raw_policy.get("AwsManaged")

        return policy["id"], policy
