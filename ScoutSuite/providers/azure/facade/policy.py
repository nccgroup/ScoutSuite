from azure.mgmt.resource.policy import PolicyClient

from ScoutSuite.core.console import print_exception
from ScoutSuite.providers.utils import run_concurrently


class PolicyFacade:
    def __init__(self, credentials, subscription_id):
        self._client = PolicyClient(credentials, subscription_id, '')

    async def get_policies_assignments(self):
        try:
            return await run_concurrently(lambda: list(self._client.policy_assignments.list()))
        except Exception as e:
            print_exception('Failed to retrieve users: {}'.format(e))
            return []
