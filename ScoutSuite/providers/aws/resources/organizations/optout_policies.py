from ScoutSuite.providers.aws.resources.base import AWSResources


class OptOutPolicies(AWSResources):
    async def fetch_all(self):
        raw_policies = await self.facade.organizations.get_optout_policies()
        for raw_policy in raw_policies:
            name, resource = self._parse_policy(raw_policy)
            self[name] = resource

    def _parse_policy(self, raw_policy):
        policy = {}
        policy["id"] = raw_policy.get("Id")
        policy["name"] = raw_policy.get("Name")
        policy["arn"] = raw_policy.get("Arn")
        if "Description" in raw_policy:
            policy["description"] = raw_policy.get("Description")
        policy["type"] = raw_policy.get("Type")
        policy["targets"] = raw_policy.get("Targets")
        policy["tags"] = raw_policy.get("Tags")
        if "children" in raw_policy:
            policy["children"] = raw_policy.get("children")
        policy["aws_managed"] = raw_policy.get("AwsManaged")

        return policy["id"], policy
