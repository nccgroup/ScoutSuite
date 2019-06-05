from google.cloud import kms

from ScoutSuite.core.console import print_exception
from ScoutSuite.providers.utils import run_concurrently


class KMSFacade:
    def __init__(self):
        self._client = kms.KeyManagementServiceClient()

    async def list_key_rings(self, project_id: str):

        try:
            # FIXME handle all locations - not sure how to list them?
            parent = self._client.location_path(project_id, 'global')
            key_rings = await run_concurrently(lambda: list(self._client.list_key_rings(parent)))
            return key_rings
        except Exception as e:
            print_exception('Failed to retrieve KMS key rings: {}'.format(e))
            return []
