from ScoutSuite.providers.aws.facade.base import AWSFacade
from ScoutSuite.providers.aws.resources.base import AWSResources
from ScoutSuite.providers.utils import get_non_provider_id


class Clusters(AWSResources):
    def __init__(self, facade: AWSFacade, region: str):
        super().__init__(facade)
        self.region = region

    async def fetch_all(self):
        raw_clusters = await self.facade.ecs.get_clusters(self.region)
        for raw_cluster in raw_clusters:
            name, resource = self._parse_cluster(raw_cluster)
            self[name] = resource

    def _parse_cluster(self, raw_cluster):
            cluster = {}
            cluster['name'] = raw_cluster['clusterName']
            cluster['status'] = raw_cluster['status']
            cluster['active_services_count'] = raw_cluster['activeServicesCount']
            cluster['registered_container_instances_count'] = raw_cluster['registeredContainerInstancesCount']
            cluster['running_tasks_count'] = raw_cluster['runningTasksCount']
            cluster['pending_tasks_count'] = raw_cluster['pendingTasksCount']
            cluster['region'] = self.region
            for setting in raw_cluster['settings']:
                 if setting['name'] == 'containerInsights':
                    if setting['value'] == 'enabled':   
                        cluster['containerInsights'] = 'True'
                    elif setting['value'] == 'disabled':
                        cluster['containerInsights'] = 'False'
                    
            return get_non_provider_id(cluster['name']), cluster
