from ScoutSuite.providers.aws.facade.base import AWSFacade
from ScoutSuite.providers.aws.resources.base import AWSResources
from ScoutSuite.providers.base.resources.base import CompositeResources
from ScoutSuite.providers.utils import get_non_provider_id


class Services(AWSResources):
    def __init__(self, facade: AWSFacade, region: str):
        super().__init__(facade)
        self.region = region
        self.cluster_arn = None

    async def fetch_all(self):
        if not self.cluster_arn:
            self.cluster_arn = await self._get_cluster_arn()
        if self.cluster_arn:
            raw_services = await self.facade.ecs.get_services(self.region, self.cluster_arn)
            for raw_service in raw_services:
                name, resource = self._parse_service(raw_service)
                self[name] = resource

    async def _get_cluster_arn(self):
        raw_clusters = await self.facade.ecs.get_clusters(self.region)
        for cluster in raw_clusters:
            if 'arn:aws:ecs' in cluster['clusterArn']:
                return cluster['clusterArn']

    def _parse_service(self, raw_service):
        service = {}
        service['name'] = raw_service['serviceName']
        service['desired_count'] = raw_service['desiredCount']
        service['running_count'] = raw_service['runningCount']
        service['pending_count'] = raw_service['pendingCount']
        service['launch_type'] = raw_service['launchType']
        service['scheduling_strategy'] = raw_service['schedulingStrategy']
        service['cluster_name'] = raw_service['clusterArn'].split("/")[-1]
        service['region'] = self.region
        service['task_defination_used'] = raw_service['deployments'][0]['taskDefinition']
        service['roll_out_state'] = raw_service['deployments'][0]['rolloutState']

        return get_non_provider_id(service['name']), service