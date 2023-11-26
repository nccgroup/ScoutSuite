from typing import Dict
from ScoutSuite.core.console import print_exception
from ScoutSuite.providers.aws.facade.utils import AWSFacadeUtils
from ScoutSuite.providers.aws.facade.basefacade import AWSBaseFacade
from ScoutSuite.providers.utils import map_concurrently, run_concurrently

class ECSFacade(AWSBaseFacade):

    async def get_clusters(self, region: str):
        ecs_client = AWSFacadeUtils.get_client('ecs', self.session, region)
        try:
            raw_clusters = await run_concurrently(ecs_client.list_clusters)
        except Exception as e:
            print(f'Failed to list ECS clusters: {e}')
            return []
        
        cluster_arns = [arn for arn in raw_clusters.get('clusterArns',[]) if arn.startswith('arn:aws:ecs:')]
        # print(cluster_arns)
        if not cluster_arns:
            return []

        return await map_concurrently(
            self._get_cluster, cluster_arns, region=region)

    async def get_services(self, region: str, cluster_arn: str):
        ecs_client = AWSFacadeUtils.get_client('ecs', self.session, region)
        try: 
            services = ecs_client.list_services(cluster=cluster_arn)
        except Exception as e:
            print(f'Failed to list ECS services: {e}')
            return []
        
        service_arns = [arn for arn in services.get('serviceArns',[]) if arn.startswith('arn:aws:ecs:')]
        if not service_arns:
            return []

        return await map_concurrently(
            self._get_service, service_arns, region=region)

    async def _get_cluster(self, cluster_arn: str, region: str) -> Dict:
        ecs_client = AWSFacadeUtils.get_client('ecs', self.session, region)
        try:
            raw_cluster = await run_concurrently(
                lambda: ecs_client.describe_clusters(clusters=[cluster_arn], include =['SETTINGS'])['clusters'][0]
            )
        except Exception as e:
            print(f'Failed to describe ECS cluster {cluster_arn}: {e}')
            return {}

        return raw_cluster

    async def _get_service(self, service_arn: str,region: str) -> Dict:
        ecs_client = AWSFacadeUtils.get_client('ecs', self.session, region)
        try:
            raw_clusters = ecs_client.list_clusters()
            clusterarn = [arn for arn in raw_clusters.get('clusterArns',[]) if arn.startswith('arn:aws:ecs:')]
            cluster_arn = "".join(clusterarn)
            raw_service = ecs_client.describe_services(services = [service_arn],cluster = cluster_arn)['services'][0]
        except Exception as e:
            print(f'Failed to describe ECS service {service_arn}: {e}')
            return {}

        return raw_service
    
    async def get_tasks(self, region: str, cluster_arn: str):
        ecs_client = AWSFacadeUtils.get_client('ecs', self.session, region)
        try: 
            tasks = ecs_client.list_tasks(cluster=cluster_arn)
        except Exception as e:
            print(f'Failed to list ECS Tasks: {e}')
            return []
        
        tasks_arns = [arn for arn in tasks.get('taskArns',[]) if arn.startswith('arn:aws:ecs:')]
        if not tasks_arns:
            return []

        return await map_concurrently(
            self._get_tasks, tasks_arns, region=region)
    
    async def _get_tasks(self, tasks_arn: str,region: str) -> Dict:
        ecs_client = AWSFacadeUtils.get_client('ecs', self.session, region)
        try:
            raw_clusters = ecs_client.list_clusters()
            clusterarn = [arn for arn in raw_clusters.get('clusterArns',[]) if arn.startswith('arn:aws:ecs:')]
            cluster_arn = "".join(clusterarn)

            raw_tasks = ecs_client.describe_tasks(tasks = [tasks_arn],cluster = cluster_arn)['tasks'][0]
        except Exception as e:
            print(f'Failed to describe ECS service {tasks_arn}: {e}')
            return {}

        return raw_tasks