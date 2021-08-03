from ScoutSuite.providers.aws.resources.base import AWSResources


class OptOutPolicies(AWSResources):
    async def fetch_all(self):
        raw_policies = await self.facade.organizations.get_optout_policies()
        for raw_policy in raw_policies:
            name, resource = self._parse_policy(raw_policy)
            self[name] = resource

    def _parse_policy(self, raw_policy):
        policy = {}
        policy["id"] = raw_policy.pop("Id")
        policy["name"] = raw_policy.pop("Name")
        policy["arn"] = raw_policy.pop("Arn")
        if "Description" in raw_policy:
            policy["description"] = raw_policy.pop("Description")
        policy["type"] = raw_policy.pop("Type")
        policy["targets"] = raw_policy.pop("Targets")
        policy["tags"] = raw_policy.pop("Tags")
        if "children" in raw_policy:
            policy["children"] = raw_policy.pop("children")
        policy["aws_managed"] = raw_policy.pop("AwsManaged")

        return policy["id"], policy
