from asyncio import Lock

from ScoutSuite.providers.aws.facade.utils import AWSFacadeUtils
from ScoutSuite.providers.aws.facade.basefacade import AWSBaseFacade
from ScoutSuite.providers.aws.utils import ec2_classic
from ScoutSuite.providers.utils import run_concurrently
from ScoutSuite.core.console import print_error, print_exception


class RDSFacade(AWSBaseFacade):
    _regional_instances_cache_locks = {}
    _instances_cache = {}
    _regional_snapshots_cache_locks = {}
    _snapshots_cache = {}
    _regional_subnet_groups_cache_locks = {}
    _subnet_groups_cache = {}

    async def get_instances(self, region: str, vpc: str):
        await self._cache_instances(region)
        return [instance for instance in self._instances_cache[region] if instance['VpcId'] == vpc]

    async def _cache_instances(self, region: str):
        async with self._regional_instances_cache_locks.setdefault(region, Lock()):
            if region in self._instances_cache:
                return

            self._instances_cache[region] = await AWSFacadeUtils.get_all_pages('rds', region, self.session, 'describe_db_instances', 'DBInstances')

            client = AWSFacadeUtils.get_client('rds', self.session, region)
            for instance in self._instances_cache[region]:
                instance['VpcId'] = instance['DBSubnetGroup']['VpcId'] \
                    if 'DBSubnetGroup' in instance and 'VpcId' in instance['DBSubnetGroup'] \
                    and instance['DBSubnetGroup']['VpcId'] \
                    else ec2_classic

                if 'DBClusterIdentifier' in instance:
                    cluster_id = instance['DBClusterIdentifier']
                    clusters = await run_concurrently(lambda: client.describe_db_clusters(DBClusterIdentifier=cluster_id))
                    cluster = clusters['DBClusters'][0]
                    instance['MultiAZ'] = cluster['MultiAZ']

    async def get_snapshots(self, region: str, vpc: str):
        await self._cache_snapshots(region)
        return [snapshot for snapshot in self._snapshots_cache[region] if snapshot['VpcId'] == vpc]

    async def _cache_snapshots(self, region: str):
        async with self._regional_snapshots_cache_locks.setdefault(region, Lock()):
            if region in self._snapshots_cache:
                return

            client = AWSFacadeUtils.get_client('rds', self.session, region)
            self._snapshots_cache[region] = await AWSFacadeUtils.get_all_pages('rds', region, self.session, 'describe_db_snapshots', 'DBSnapshots')
            for snapshot in self._snapshots_cache[region]:
                snapshot_id = snapshot['DBSnapshotIdentifier']
                snapshot['VpcId'] = snapshot['VpcId'] if 'VpcId' in snapshot else ec2_classic
                attributes_response = await run_concurrently(lambda: client.describe_db_snapshot_attributes(DBSnapshotIdentifier=snapshot_id))
                attributes = attributes_response['DBSnapshotAttributesResult']
                snapshot['Attributes'] = attributes['DBSnapshotAttributes'] if 'DBSnapshotAttributes' in attributes else {}

    async def get_subnet_groups(self, region: str, vpc: str):
        await self._cache_subnet_groups(region)
        return [subnet_group for subnet_group in self._subnet_groups_cache[region] if subnet_group['VpcId'] == vpc]

    async def _cache_subnet_groups(self, region: str):
        async with self._regional_subnet_groups_cache_locks.setdefault(region, Lock()):
            if region in self._subnet_groups_cache:
                return

            self._subnet_groups_cache[region] = await AWSFacadeUtils.get_all_pages('rds', region, self.session, 'describe_db_subnet_groups', 'DBSubnetGroups')
                
    async def get_parameter_groups(self, region: str):
        parameter_groups = await AWSFacadeUtils.get_all_pages('rds', region, self.session, 'describe_db_parameter_groups', 'DBParameterGroups')
        for parameter_group in parameter_groups:
            name = parameter_group['DBParameterGroupName']
            try:
                parameters = await AWSFacadeUtils.get_all_pages('rds', region, self.session, 'describe_db_parameters', 'Parameters', DBParameterGroupName=name)
                parameter_group['Parameters'] = {}
                for parameter in parameters:
                    # Discard non-modifiable parameters
                    if not parameter['IsModifiable']:
                        continue
                    parameter_name = parameter.pop('ParameterName')
                    parameter_group['Parameters'][parameter_name] = parameter
            except Exception as e:
                print_exception(e)
                print_error('Failed fetching DB parameters for %s' % name)

        return parameter_groups

    async def get_security_groups(self, region: str) :
        return await AWSFacadeUtils.get_all_pages('rds', region, self.session, 'describe_db_security_groups', 'DBSecurityGroups')
