from google.cloud import kms

from ScoutSuite.core.console import print_exception
from ScoutSuite.providers.gcp.facade.basefacade import GCPBaseFacade
from ScoutSuite.providers.gcp.facade.utils import GCPFacadeUtils
from ScoutSuite.providers.utils import run_concurrently


class KMSFacade(GCPBaseFacade):
    def __init__(self):
        # This facade is currently using both libraries as the Cloud Client library doesn't support locations
        self.cloud_client = kms.KeyManagementServiceClient()  # Cloud Client
        super(KMSFacade, self).__init__('cloudkms', 'v1')  # API Client

    async def get_locations(self, project_id: str):

        try:
            kms_client = self._get_client()
            parent = 'projects/{}'.format(project_id)
            locations = kms_client.projects().locations()
            request = locations.list(name=parent)
            return await GCPFacadeUtils.get_all('locations', request, locations)
        except Exception as e:
            print_exception('Failed to retrieve KMS locations: {}'.format(e))
            return []

    async def list_key_rings(self, project_id: str):

        try:
            locations = await self.get_locations(project_id)
            key_rings = {}
            for l in locations:
                parent = self.cloud_client.location_path(project_id, l['locationId'])
                key_rings[l['locationId']] = await run_concurrently(
                    lambda: list(self.cloud_client.list_key_rings(parent)))
            return key_rings
        except Exception as e:
            print_exception('Failed to retrieve KMS key rings: {}'.format(e))
            return {}

    async def list_keys(self, project_id: str, location: str, keyring_name: str):

        try:
            parent = self.cloud_client.key_ring_path(project_id, location, keyring_name)
            kms_client = self._get_client()
            cryptokeys = kms_client.projects().locations().keyRings().cryptoKeys()
            request = cryptokeys.list(parent=parent)
            return await GCPFacadeUtils.get_all('cryptoKeys', request, cryptokeys)
        except Exception as e:
            print_exception('Failed to retrieve KMS keys for key ring {}: {}'.format(keyring_name, e))
            return []
