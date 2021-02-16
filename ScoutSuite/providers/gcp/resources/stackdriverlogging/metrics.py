from ScoutSuite.providers.base.resources.base import Resources
from ScoutSuite.providers.gcp.facade.base import GCPFacade
from ScoutSuite.core.console import print_exception


class Metrics(Resources):
    def __init__(self, facade: GCPFacade, project_id: str):
        super().__init__(facade)
        self.project_id = project_id

    async def fetch_all(self):
        raw_metrics = await self.facade.stackdriverlogging.get_metrics(self.project_id)
        parsing_error_counter = 0
        for raw_metric in raw_metrics:
            try:
                metric_name, metric = self._parse_metric(raw_metric)
                self[metric_name] = metric
            except Exception as e:
                parsing_error_counter += 1
        if parsing_error_counter > 0:
            print_exception(
                'Failed to parse {} resource: {} times'.format(self.__class__.__name__, parsing_error_counter))

    def _parse_metric(self, raw_metric):
        metric_dict = {}
        metric_dict['name'] = raw_metric.name
        metric_dict['description'] = raw_metric.description
        metric_dict['filter'] = raw_metric.filter_
        return metric_dict['name'], metric_dict
