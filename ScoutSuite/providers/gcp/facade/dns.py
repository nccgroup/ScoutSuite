from ScoutSuite.core.console import print_exception
from ScoutSuite.providers.gcp.facade.basefacade import GCPBaseFacade
from ScoutSuite.providers.gcp.facade.utils import GCPFacadeUtils
from ScoutSuite.providers.utils import run_concurrently


class DNSFacade(GCPBaseFacade):
    def __init__(self):
        super().__init__('dns', 'v1')

    async def get_zones(self, project_id):
        try:
            dns_client = self._get_client()
            return await run_concurrently(
                lambda: dns_client.managedZones().list(project=project_id).execute()
            )
        except Exception as e:
            print_exception(f'Failed to retrieve zones: {e}')
            return {}
