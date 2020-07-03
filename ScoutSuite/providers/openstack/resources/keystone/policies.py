from ScoutSuite.providers.openstack.resources.base import OpenstackResources


class Policies(OpenstackResources):
    async def fetch_all(self):
        raw_policies = await self.facade.keystone.get_policies()
        for raw_policy in raw_policies:
            id, policy = self._parse_policy(raw_policy)
            if id in self:
                continue

            self[id] = policy

    def _parse_policy(self, raw_policy):
        policy_dict = {}
        policy_dict['id'] = raw_policy.id
        policy_dict['rules'] = raw_policy.blob
        return policy_dict['id'], policy_dict
