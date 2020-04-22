from asyncio import Lock

from botocore.exceptions import ClientError

from ScoutSuite.core.console import print_exception
from ScoutSuite.providers.aws.facade.basefacade import AWSBaseFacade
from ScoutSuite.providers.aws.facade.utils import AWSFacadeUtils
from ScoutSuite.providers.aws.utils import ec2_classic
from ScoutSuite.providers.utils import get_and_set_concurrently


class ElastiCacheFacade(AWSBaseFacade):
    regional_clusters_cache_locks = {}
    regional_subnets_cache_locks = {}
    clusters_cache = {}
    subnets_cache = {}

    async def get_clusters(self, region, vpc):
        await self.cache_clusters(region)
        return [cluster for cluster in self.clusters_cache[region] if cluster['VpcId'] == vpc]

    async def cache_clusters(self, region):
        async with self.regional_clusters_cache_locks.setdefault(region, Lock()):
            if region in self.clusters_cache:
                return

            self.clusters_cache[region] = await AWSFacadeUtils.get_all_pages(
                'elasticache', region, self.session, 'describe_cache_clusters', 'CacheClusters')

            await get_and_set_concurrently(
                [self._get_and_set_cluster_vpc], self.clusters_cache[region], region=region)

    async def _get_and_set_cluster_vpc(self, cluster: {}, region: str):
        if 'CacheSubnetGroupName' not in cluster:
            cluster['VpcId'] = ec2_classic
        else:
            subnets = await AWSFacadeUtils.get_all_pages(
                'elasticache', region, self.session, 'describe_cache_subnet_groups', 'CacheSubnetGroups',
                CacheSubnetGroupName=cluster['CacheSubnetGroupName'])
            subnet_group = subnets[0]
            cluster['VpcId'] = subnet_group['VpcId']

    async def get_security_groups(self, region):
        client = AWSFacadeUtils.get_client('elasticache', self.session, region)

        try:
            return await AWSFacadeUtils.get_all_pages(
                'elasticache', region, self.session, 'describe_cache_security_groups', 'CacheSecurityGroups')
        except client.exceptions.InvalidParameterValueException:
            # Recent account are not allowed to use security groups at this level. Calling
            # describe_cache_security_groups will throw an InvalidParameterValueException exception.
            pass
        except Exception as e:
            print_exception('Failed to get ElastiCache security groups: {}'.format(e))

        return []

    async def get_subnet_groups(self, region, vpc):
        await self.cache_subnets(region)
        return [subnet for subnet in self.subnets_cache[region] if subnet['VpcId'] == vpc]

    async def cache_subnets(self, region):
        async with self.regional_subnets_cache_locks.setdefault(region, Lock()):
            if region in self.subnets_cache:
                return

            self.subnets_cache[region] = await AWSFacadeUtils.get_all_pages(
                'elasticache', region, self.session, 'describe_cache_subnet_groups', 'CacheSubnetGroups')

    async def get_parameter_groups(self, region):

        # If EC2-Classic isn't available (e.g., a new account)
        # this method will fail with:
        #   Code:    "InvalidParameterValue"
        #   Message: "Use of cache security groups is not permitted in
        #             this API version for your account."
        #   Type:    "Sender"
        try:
            return await AWSFacadeUtils.get_all_pages(
                'elasticache', region, self.session, 'describe_cache_parameter_groups', 'CacheParameterGroups')
        except ClientError as e:
            if e.response['Error']['Code'] != 'InvalidParameterValue':
                print_exception('Failed to describe cache parameter groups: {}'.format(e))
            return []
