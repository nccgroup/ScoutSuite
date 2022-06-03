from ScoutSuite.core.console import print_exception
from ScoutSuite.providers.gcp.facade.basefacade import GCPBaseFacade
from ScoutSuite.providers.gcp.facade.utils import GCPFacadeUtils
from ScoutSuite.providers.utils import map_concurrently, run_concurrently


class BigQueryFacade(GCPBaseFacade):
    def __init__(self):

        super().__init__('bigquery', 'v2')  # API Client

    async def get_datasets(self, project_id: str):
        try:
            bigquery_client = self._get_client()
            datasets = bigquery_client.datasets()

            # get list of datasets
            request = datasets.list(projectId=project_id)
            results = await GCPFacadeUtils.get_all('datasets', request, datasets)
            # extract ids
            dataset_ids = [dataset.get('id').split(':')[-1] for dataset in results]
        except Exception as e:
            print_exception(f'Failed to list BigQuery datasets: {e}')
            return []
        else:
            return await map_concurrently(self._get_dataset, dataset_ids, project_id=project_id)

    async def _get_dataset(self, dataset_id: str, project_id: str):
        try:
            bigquery_client = self._get_client()
            datasets = bigquery_client.datasets()
            request = datasets.get(projectId=project_id, datasetId=dataset_id)
            return await run_concurrently(
                lambda: request.execute()
            )
        except Exception as e:
            print_exception(f'Failed to retrieve BigQuery datasets {dataset_id}: {e}')
            return {}
