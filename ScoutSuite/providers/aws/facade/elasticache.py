import boto3

from ScoutSuite.providers.aws.facade.utils import AWSFacadeUtils
from ScoutSuite.providers.aws.facade.basefacade import AWSBaseFacade
from ScoutSuite.providers.aws.utils import ec2_classic
from asyncio import Lock

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
            
            self.clusters_cache[region] = await AWSFacadeUtils.get_all_pages('elasticache', region, self.session, 'describe_cache_clusters', 'CacheClusters')

            for cluster in self.clusters_cache[region]:
                if 'CacheSubnetGroupName' not in cluster:
                    cluster['VpcId'] = ec2_classic
                else:
                    subnet_group = await self.get_subnet_group(region, cluster['CacheSubnetGroupName'])
                    cluster['VpcId'] = subnet_group['VpcId']

    async def get_security_groups(self, region):
        client = AWSFacadeUtils.get_client('elasticache', region, self.session)

        try:
            return await AWSFacadeUtils.get_all_pages('elasticache', region, self.session, 'describe_cache_security_groups', 'CacheSecurityGroups')

        except client.exceptions.InvalidParameterValueException:
            # Recent account are not allowed to use security groups at this level. Calling
            # describe_cache_security_groups will throw an InvalidParameterValueException exception.
            pass

        return []

    async def get_subnet_groups(self, region, vpc):
        await self.cache_subnets(region)
        return [subnet for subnet in self.subnets_cache[region] if subnet['VpcId'] == vpc]

    async def get_subnet_group(self, region, subnet_name):
        subnets = await AWSFacadeUtils.get_all_pages('elasticache', \
                                                  region, \
                                                  self.session, \
                                                  'describe_cache_subnet_groups', \
                                                  'CacheSubnetGroups', \
                                                  CacheSubnetGroupName=subnet_name \
                                                )
        return subnets[0]

    async def cache_subnets(self, region):
        async with self.regional_subnets_cache_locks.setdefault(region, Lock()):
            if region in self.subnets_cache:
                return
            
            self.subnets_cache[region] = await AWSFacadeUtils.get_all_pages('elasticache', region, self.session, 'describe_cache_subnet_groups', 'CacheSubnetGroups')

    async def get_parameter_groups(self, region):
        return await AWSFacadeUtils.get_all_pages('elasticache', region, self.session, 'describe_cache_parameter_groups', 'CacheParameterGroups')