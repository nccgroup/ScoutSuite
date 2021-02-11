from ScoutSuite.providers.oci.facade.base import OracleFacade
from ScoutSuite.providers.oci.resources.base import OracleResources
from ScoutSuite.providers.utils import get_non_provider_id
from ScoutSuite.core.console import print_exception


class Policies(OracleResources):
    def __init__(self, facade: OracleFacade):
        super().__init__(facade)

    async def fetch_all(self):
        parsing_error_counter = 0
        for raw_policy in await self.facade.identity.get_policies():
            try:
                id, policy = await self._parse_policy(raw_policy)
                self[id] = policy
            except Exception as e:
                parsing_error_counter += 1
        if parsing_error_counter > 0:
            print_exception(
                'Failed to parse {} resource: {} times'.format(self.__class__.__name__, parsing_error_counter))

    async def _parse_policy(self, raw_policy):
        policy = {}
        policy['id'] = get_non_provider_id(raw_policy.id)
        policy['identifier'] = raw_policy.id
        policy['name'] = raw_policy.name
        policy['description'] = raw_policy.description
        policy['statements'] = [s.lower() for s in raw_policy.statements]
        policy['state'] = raw_policy.lifecycle_state
        return policy['id'], policy
