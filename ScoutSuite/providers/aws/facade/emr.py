from ScoutSuite.providers.aws.facade.utils import AWSFacadeUtils
from ScoutSuite.providers.aws.facade.basefacade import AWSBaseFacade
from ScoutSuite.providers.utils import run_concurrently


class EMRFacade(AWSBaseFacade):
    async def get_clusters(self, region):
        clusters_list = await AWSFacadeUtils.get_all_pages('emr', region, self.session, 'list_clusters', 'Clusters')
        client = AWSFacadeUtils.get_client('emr', region, self.session)
        clusters_descriptions = []
        for cluster_id in [cluster['Id'] for cluster in clusters_list]:
            cluster = client.describe_cluster(ClusterId=cluster_id)['Cluster']
            clusters_descriptions.append(cluster)

        return clusters_descriptions
