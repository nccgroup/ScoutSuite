from ScoutSuite.providers.base.resources.base import Resources
from ScoutSuite.providers.gcp.facade.base import GCPFacade


class Datasets(Resources):
    def __init__(self, facade: GCPFacade, project_id: str):
        super().__init__(facade)
        self.project_id = project_id

    async def fetch_all(self):
        raw_datasets = await self.facade.bigquery.get_datasets(self.project_id)
        for raw_dataset in raw_datasets:
            dataset_id, dataset = self._parse_dataset(raw_dataset)
            self[dataset_id] = dataset

    def _parse_dataset(self, raw_dataset):
        print()
        print(raw_dataset)
        return None, None
