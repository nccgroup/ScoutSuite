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
        service['name'] = raw_service.get('serviceName', 'N/A')
        service['desired_count'] = raw_service.get('desiredCount', 0)
        service['running_count'] = raw_service.get('runningCount', 0)
        service['pending_count'] = raw_service.get('pendingCount', 0)
        # launchType is optional when using capacity provider strategies
        service['launch_type'] = raw_service.get('launchType', 'N/A')
        service['scheduling_strategy'] = raw_service.get('schedulingStrategy', 'REPLICA')
        service['cluster_name'] = raw_service.get('clusterArn', '').split("/")[-1] if raw_service.get('clusterArn') else 'N/A'
        service['region'] = self.region

        # Parse deployment information if deployments exist
        if raw_service.get('deployments') and len(raw_service['deployments']) > 0:
            deployment = raw_service['deployments'][0]
            service['task_defination_used'] = deployment.get('taskDefinition', 'N/A')
            service['roll_out_state'] = deployment.get('rolloutState', 'UNKNOWN')
        else:
            service['task_defination_used'] = 'N/A'
            service['roll_out_state'] = 'UNKNOWN'

        return get_non_provider_id(service['name']), service