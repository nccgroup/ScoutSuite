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
        task['arn'] = raw_task.get('taskArn', '')
        task['taskDefinitionArn'] = raw_task.get('taskDefinitionArn', '')
        task['last_status'] = raw_task.get('lastStatus', 'UNKNOWN')
        task['healthStatus'] = raw_task.get('healthStatus', 'UNKNOWN')
        task['desiredStatus'] = raw_task.get('desiredStatus', 'UNKNOWN')
        task['task_cpu'] = raw_task.get('cpu', 'N/A')
        task['cluster_arn'] = raw_task.get('clusterArn', '')
        task['task_launchType'] = raw_task.get('launchType', 'UNKNOWN')
        task['region'] = self.region
        task['availabilityZone'] = raw_task.get('availabilityZone', 'N/A')
        # containerInstanceArn only exists for EC2 launch type, not Fargate
        task['containerInstanceArn'] = raw_task.get('containerInstanceArn', 'N/A')

        # Parse container information if containers exist
        if raw_task.get('containers') and len(raw_task['containers']) > 0:
            container = raw_task['containers'][0]
            task['containerArn'] = container.get('containerArn', 'N/A')
            task['container_name'] = container.get('name', 'N/A')
            task['container_image_name'] = container.get('image', 'N/A')
            task['container_lastStatus'] = container.get('lastStatus', 'UNKNOWN')
            task['container_healthStatus'] = container.get('healthStatus', 'UNKNOWN')
        else:
            task['containerArn'] = 'N/A'
            task['container_name'] = 'N/A'
            task['container_image_name'] = 'N/A'
            task['container_lastStatus'] = 'UNKNOWN'
            task['container_healthStatus'] = 'UNKNOWN'

        return get_non_provider_id(task['arn']), task