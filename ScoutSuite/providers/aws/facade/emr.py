from ScoutSuite.providers.aws.facade.utils import AWSFacadeUtils
from ScoutSuite.providers.aws.facade.basefacade import AWSBaseFacade
from ScoutSuite.providers.utils import map_concurrently, run_concurrently


class EMRFacade(AWSBaseFacade):
    async def get_clusters(self, region):
        cluster_list = await AWSFacadeUtils.get_all_pages('emr', region, self.session, 'list_clusters', 'Clusters')
        cluster_ids = [cluster['Id'] for cluster in cluster_list]
        client = AWSFacadeUtils.get_client('emr', self.session, region)

        return await map_concurrently(
            lambda cluster_id: run_concurrently(
                lambda: client.describe_cluster(ClusterId=cluster_id)['Cluster']),
            cluster_ids)
