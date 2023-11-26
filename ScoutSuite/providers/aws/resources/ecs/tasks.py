from ScoutSuite.providers.aws.facade.base import AWSFacade
from ScoutSuite.providers.aws.resources.base import AWSResources
from ScoutSuite.providers.base.resources.base import CompositeResources
from ScoutSuite.providers.utils import get_non_provider_id

class Tasks(AWSResources):
    def __init__(self, facade: AWSFacade, region: str):
        super().__init__(facade)
        self.region = region
        self.cluster_arn = None

    async def fetch_all(self):
        if not self.cluster_arn:
            self.cluster_arn = await self._get_cluster_arn()
        if self.cluster_arn:
            raw_tasks = await self.facade.ecs.get_tasks(self.region, self.cluster_arn)
            for raw_task in raw_tasks:
                name, resource = self._parse_tasks(raw_task)
                self[name] = resource

    async def _get_cluster_arn(self):
        raw_clusters = await self.facade.ecs.get_clusters(self.region)
        for cluster in raw_clusters:
            if 'arn:aws:ecs' in cluster['clusterArn']:
                return cluster['clusterArn']

    def _parse_tasks(self, raw_task):
        task = {}
        task['arn'] = raw_task['taskArn']
        task['taskDefinitionArn'] = raw_task['taskDefinitionArn']
        task['last_status'] = raw_task['lastStatus']
        task['healthStatus'] = raw_task['healthStatus']
        task['desiredStatus'] = raw_task['desiredStatus']
        task['task_cpu'] = raw_task['cpu']
        task['cluster_arn'] = raw_task['clusterArn']
        task['task_launchType'] = raw_task['launchType']
        task['region'] = self.region
        task['availabilityZone'] = raw_task['availabilityZone']
        task['containerInstanceArn'] = raw_task['containerInstanceArn']
        task['containerArn'] = raw_task['containers'][0]['containerArn']
        task['container_name'] = raw_task['containers'][0]['name']
        task['container_image_name'] = raw_task['containers'][0]['image']
        task['container_lastStatus'] = raw_task['containers'][0]['lastStatus']
        task['container_healthStatus'] = raw_task['containers'][0]['healthStatus']

        return get_non_provider_id(task['arn']), task