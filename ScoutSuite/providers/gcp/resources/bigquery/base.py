from ScoutSuite.providers.gcp.resources.bigquery.datasets import Datasets
from ScoutSuite.providers.gcp.resources.projects import Projects


class BigQuery(Projects):
    _children = [
        (Datasets, 'datasets')
    ]
