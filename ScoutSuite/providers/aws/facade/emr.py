from ScoutSuite.providers.aws.facade.utils import AWSFacadeUtils
from ScoutSuite.providers.aws.facade.basefacade import AWSBaseFacade
from ScoutSuite.providers.utils import run_concurrently, run_tasks_concurrently
import asyncio


class EMRFacade(AWSBaseFacade):
    async def get_clusters(self, region):
        clusters_list = await AWSFacadeUtils.get_all_pages('emr', region, self.session, 'list_clusters', 'Clusters')
        client = AWSFacadeUtils.get_client('emr', self.session, region)
        cluster_ids = [cluster['Id'] for cluster in clusters_list]
        
        return await run_tasks_concurrently({
            run_concurrently(lambda: client.describe_cluster(ClusterId=id)['Cluster']) for id in cluster_ids
        })
