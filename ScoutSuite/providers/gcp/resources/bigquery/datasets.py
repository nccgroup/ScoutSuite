from ScoutSuite.providers.base.resources.base import Resources
from ScoutSuite.providers.gcp.facade.base import GCPFacade
from ScoutSuite.providers.utils import get_non_provider_id


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
        dataset_dict = {}
        dataset_dict['id'] = get_non_provider_id(raw_dataset.get('id'))
        dataset_dict['name'] = raw_dataset.get('datasetReference').get('datasetId')
        dataset_dict['location'] = raw_dataset.get('location')
        dataset_dict['creation_time'] = int(raw_dataset.get('creationTime'))
        dataset_dict['last_modified_time'] = int(raw_dataset.get('lastModifiedTime'))
        dataset_dict['default_encryption_configuration'] = \
            raw_dataset.get('defaultEncryptionConfiguration', {}).get('kmsKeyName')

        # format bindings in a way that's easier to query
        dataset_dict['bindings'] = {}
        for entry in raw_dataset.get('access'):
            role = entry.get('role')
            if role not in dataset_dict['bindings'].keys():
                dataset_dict['bindings'][role] = []
            for k, v in entry.items():
                if k != 'role':
                    dataset_dict['bindings'][role].append({"type": k,
                                                           "member": v})

        return dataset_dict['id'], dataset_dict
