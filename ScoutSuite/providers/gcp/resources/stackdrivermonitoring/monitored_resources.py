from ScoutSuite.providers.base.resources.base import Resources
from ScoutSuite.providers.gcp.facade.base import GCPFacade


class MonitoredResources(Resources):
    def __init__(self, facade: GCPFacade, project_id: str):
        super(MonitoredResources, self).__init__(facade)
        self.project_id = project_id

    async def fetch_all(self):
        raw_monitored_resources = await self.facade.stackdrivermonitoring.get_monitored_resources(self.project_id)
        for raw_monitored_resource in raw_monitored_resources:
            monitored_resource_name, monitored_resource = self._parse_monitored_resource(raw_monitored_resource)
            self[monitored_resource_name] = monitored_resource

    def _parse_monitored_resource(self, raw_monitored_resource):
        monitored_resource_dict = {}
        monitored_resource_dict['name'] = raw_monitored_resource.display_name
        monitored_resource_dict['description'] = raw_monitored_resource.description
        return monitored_resource_dict['name'], monitored_resource_dict
