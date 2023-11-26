from typing import Dict
from ScoutSuite.providers.aws.facade.basefacade import AWSBaseFacade
from ScoutSuite.providers.aws.facade.utils import AWSFacadeUtils
from ScoutSuite.providers.utils import run_concurrently,map_concurrently


class EKSFacade(AWSBaseFacade):

    async def get_clusters(self, region: str):
        eks_client = AWSFacadeUtils.get_client('eks', self.session, region)
        try:
            raw_clusters = await run_concurrently(eks_client.list_clusters)
        except Exception as e:
            print(f'Failed to list EKS clusters: {e}')
            return []

        cluster_name = [name for name in raw_clusters.get('clusters',[])]
        if not cluster_name:
            return []

        return await map_concurrently(
            self._get_cluster, cluster_name, region=region)

    async def get_nodegroups(self, region: str, cluster_name: str):
        eks_client = AWSFacadeUtils.get_client('eks', self.session, region)
        try: 
            nodegroups = eks_client.list_nodegroups(clusterName=cluster_name)
        except Exception as e:
            print(f'Failed to list ECS services: {e}')
            return []
        
        node_name = [name for name in nodegroups.get('nodegroups',[])]
        if not node_name:
            return []

        return await map_concurrently(
            self._get_nodegroup, node_name, region=region)

    async def _get_cluster(self, cluster_name: str, region: str) -> Dict:
        eks_client = AWSFacadeUtils.get_client('eks', self.session, region)
        try:
            raw_cluster = await run_concurrently(
                lambda: eks_client.describe_cluster(name = cluster_name))
            
        except Exception as e:
            print(f'Failed to describe EKS cluster {cluster_name}: {e}')
            return {}

        return raw_cluster

    async def _get_nodegroup(self, node_name: str, region: str) -> Dict:
        eks_client = AWSFacadeUtils.get_client('eks', self.session, region)
        try:
            raw_clusters = eks_client.list_clusters()
            clusterarn = [arn for arn in raw_clusters.get('clusters',[])]
            cluster_name = "".join(clusterarn)
           
            raw_nodedata = eks_client.describe_nodegroup(nodegroupName = node_name,clusterName = cluster_name)['nodegroup']
        except Exception as e:
            print(f'Failed to describe EKS nodegroup {node_name}: {e}')
            return {}

        return raw_nodedata