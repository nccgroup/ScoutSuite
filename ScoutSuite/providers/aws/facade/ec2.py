import base64
import asyncio

from ScoutSuite.providers.aws.facade.utils import AWSFacadeUtils
from ScoutSuite.providers.utils import run_concurrently
from ScoutSuite.providers.aws.facade.basefacade import AWSBaseFacade


class EC2Facade(AWSBaseFacade):
    regional_flow_logs_cache_locks = {}
    flow_logs_cache = {}

    async def get_instance_user_data(self, region: str, instance_id: str):
        ec2_client = AWSFacadeUtils.get_client('ec2', self.session, region)
        user_data_response = await run_concurrently(
            lambda: ec2_client.describe_instance_attribute(Attribute='userData', InstanceId=instance_id))

        if 'Value' not in user_data_response['UserData'].keys():
            return None

        return base64.b64decode(user_data_response['UserData']['Value']).decode('utf-8')

    async def get_instances(self, region: str, vpc: str):
        filters = [{'Name': 'vpc-id', 'Values': [vpc]}]
        reservations =\
            await AWSFacadeUtils.get_all_pages(
                'ec2', region, self.session, 'describe_instances', 'Reservations', Filters=filters)

        instances = []
        for reservation in reservations:
            for instance in reservation['Instances']:
                instance['ReservationId'] = reservation['ReservationId']
                instances.append(instance)
                
        return instances

    async def get_security_groups(self, region: str, vpc: str):
        filters = [{'Name': 'vpc-id', 'Values': [vpc]}]
        return await AWSFacadeUtils.get_all_pages(
            'ec2', region, self.session, 'describe_security_groups', 'SecurityGroups', Filters=filters)

    async def get_vpcs(self, region: str):
        ec2_client = AWSFacadeUtils.get_client('ec2', region, self.session)
        return await run_concurrently(lambda: ec2_client.describe_vpcs()['Vpcs'])

    async def get_images(self, region: str, owner_id: str):
        filters = [{'Name': 'owner-id', 'Values': [owner_id]}]
        client = AWSFacadeUtils.get_client('ec2', self.session, region)
        response = await run_concurrently(lambda: client.describe_images(Filters=filters))

        return response['Images']

    async def get_network_interfaces(self, region: str, vpc: str):
        filters = [{'Name': 'vpc-id', 'Values': [vpc]}]
        return await AWSFacadeUtils.get_all_pages(
            'ec2', region, self.session, 'describe_network_interfaces', 'NetworkInterfaces', Filters=filters)

    async def get_volumes(self, region: str):
        return await AWSFacadeUtils.get_all_pages('ec2', region, self.session, 'describe_volumes', 'Volumes')

    async def get_snapshots(self, region: str, owner_id: str):
        filters = [{'Name': 'owner-id', 'Values': [owner_id]}]
        snapshots = await AWSFacadeUtils.get_all_pages(
            'ec2', region, self.session, 'describe_snapshots', 'Snapshots', Filters=filters)

        ec2_client = AWSFacadeUtils.get_client('ec2', self.session, region)
        for snapshot in snapshots:
            snapshot['CreateVolumePermissions'] = await run_concurrently(lambda: ec2_client.describe_snapshot_attribute(
                Attribute='createVolumePermission',
                SnapshotId=snapshot['SnapshotId'])['CreateVolumePermissions'])

        return snapshots

    async def get_network_acls(self, region: str, vpc: str):
        filters = [{'Name': 'vpc-id', 'Values': [vpc]}]
        return await AWSFacadeUtils.get_all_pages(
            'ec2', region, self.session, 'describe_network_acls', 'NetworkAcls', Filters=filters)

    async def get_flow_logs(self, region: str):
        await self.cache_flow_logs(region)
        return self.flow_logs_cache[region]

    async def cache_flow_logs(self, region: str):
        async with self.regional_flow_logs_cache_locks.setdefault(region, asyncio.Lock()):
            if region in self.flow_logs_cache:
                return

            self.flow_logs_cache[region] =\
                await AWSFacadeUtils.get_all_pages('ec2', region, self.session, 'describe_flow_logs', 'FlowLogs')

    async def get_subnets(self, region: str, vpc: str):
        ec2_client = AWSFacadeUtils.get_client('ec2', region, self.session)
        filters = [{'Name': 'vpc-id', 'Values': [vpc]}]
        subnets = await run_concurrently(
            lambda: ec2_client.describe_subnets(Filters=filters)['Subnets']
        )
        # Fetch and set subnet flow logs concurrently:
        tasks = {
            asyncio.ensure_future(
                self.get_and_set_subnet_flow_logs(region, subnet)
            ) for subnet in subnets
        }
        await asyncio.wait(tasks)

        return subnets

    async def get_and_set_subnet_flow_logs(self, region: str, subnet: {}):
        await self.cache_flow_logs(region)
        subnet['flow_logs'] =\
            [flow_log for flow_log in self.flow_logs_cache[region]
             if flow_log['ResourceId'] == subnet['SubnetId'] or flow_log['ResourceId'] == subnet['VpcId']]
