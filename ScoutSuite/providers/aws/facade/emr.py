from ScoutSuite.providers.aws.facade.utils import AWSFacadeUtils
from ScoutSuite.providers.aws.facade.basefacade import AWSBaseFacade
from ScoutSuite.providers.utils import run_concurrently
import asyncio


class EMRFacade(AWSBaseFacade):
    async def get_clusters(self, region):
        clusters_list = await AWSFacadeUtils.get_all_pages('emr', region, self.session, 'list_clusters', 'Clusters')
        client = AWSFacadeUtils.get_client('emr', self.session, region)
        clusters_descriptions = []
        cluster_ids = [cluster['Id'] for cluster in clusters_list]
        tasks = {
                asyncio.ensure_future(
                        run_concurrently(lambda: client.describe_cluster(ClusterId=cluster_id)['Cluster'])
                 ) for cluster_id in cluster_ids
        }
        for task in asyncio.as_completed(tasks):
                cluster = await task
                clusters_descriptions.append(cluster)

        return clusters_descriptions
