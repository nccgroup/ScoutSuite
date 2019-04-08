from ScoutSuite.core.console import print_exception
from ScoutSuite.providers.aws.facade.basefacade import AWSBaseFacade
from ScoutSuite.providers.aws.facade.utils import AWSFacadeUtils
from ScoutSuite.providers.utils import map_concurrently, run_concurrently


class EMRFacade(AWSBaseFacade):
    async def get_clusters(self, region):
        cluster_list = await AWSFacadeUtils.get_all_pages('emr', region, self.session, 'list_clusters', 'Clusters')
        cluster_ids = [cluster['Id'] for cluster in cluster_list]
        client = AWSFacadeUtils.get_client('emr', self.session, region)

        try:
            return await map_concurrently(
                lambda cluster_id: run_concurrently(
                    lambda: client.describe_cluster(ClusterId=cluster_id)['Cluster']),
                cluster_ids)
        except Exception as e:
            print_exception('Failed to describe EMR cluster: {}'.format(e))
            return []
