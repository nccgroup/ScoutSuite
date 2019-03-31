from asyncio import Lock

from ScoutSuite.providers.aws.facade.utils import AWSFacadeUtils
from ScoutSuite.providers.aws.facade.basefacade import AWSBaseFacade
from ScoutSuite.providers.aws.utils import ec2_classic
from botocore.utils import ClientError


class RedshiftFacade(AWSBaseFacade):
    regional_cluster_cache_locks = {}
    clusters_cache = {}

    async def get_clusters(self, region: str, vpc: str):
        await self.cache_clusters(region)
        return [cluster for cluster in self.clusters_cache[region] if cluster['VpcId'] == vpc]

    async def cache_clusters(self, region):
        async with self.regional_cluster_cache_locks.setdefault(region, Lock()):
            if region in self.clusters_cache:
                return

            self.clusters_cache[region] = await AWSFacadeUtils.get_all_pages(
                'redshift', region, self.session, 'describe_clusters', 'Clusters')

            for cluster in self.clusters_cache[region]:
                cluster['VpcId'] =\
                    cluster['VpcId'] if 'VpcId' in cluster and cluster['VpcId'] else ec2_classic

    async def get_cluster_parameter_groups(self, region: str):
        return await AWSFacadeUtils.get_all_pages(
            'redshift', region, self.session, 'describe_cluster_parameter_groups', 'ParameterGroups')

    async def get_cluster_security_groups(self, region: str):
        # For VPC-by-default customers, describe_cluster_parameters will throw an exception. Just try and ignore it:
        try:
            return await AWSFacadeUtils.get_all_pages(
                'redshift', region, self.session, 'describe_cluster_security_groups', 'ClusterSecurityGroups')
        except ClientError:
            return []

    async def get_cluster_parameters(self, region: str, parameter_group: str):
        return await AWSFacadeUtils.get_all_pages(
            'redshift', region, self.session, 'describe_cluster_parameters', 'Parameters',
            ParameterGroupName=parameter_group)
