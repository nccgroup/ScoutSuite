from ScoutSuite.providers.azure.resources.base import AzureResources


class PolicyAssignments(AzureResources):
    async def fetch_all(self):
        for raw_policy in await self.facade.policies.get_policies_assignments():
            id, policy = self._parse_policy(raw_policy)
            self[id] = policy

    def _parse_policy(self, raw_policy):
        policy = {}
        policy['id'] = raw_policy.id

        return policy['id'], policy