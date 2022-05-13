from google.cloud import kms
from google.api_core.gapic_v1.client_info import ClientInfo

from ScoutSuite.core.console import print_exception
from ScoutSuite.providers.gcp.facade.basefacade import GCPBaseFacade
from ScoutSuite.providers.gcp.facade.utils import GCPFacadeUtils
from ScoutSuite.providers.utils import run_concurrently
from ScoutSuite.utils import get_user_agent


class BigQueryFacade(GCPBaseFacade):
    def __init__(self):

        super().__init__('bigquery', 'v2')  # API Client


    async def get_datasets(self, project_id: str):
        try:
            bigquery_client = self._get_client()

            datasets = bigquery_client.datasets()
            request = datasets.list(projectId=project_id)
            results = await GCPFacadeUtils.get_all('datasets', request, datasets)
            return results

        except Exception as e:
            print_exception(f'Failed to retrieve BigQuery datasets): {e}')
            return []
