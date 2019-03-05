import boto3
import base64

from ScoutSuite.providers.aws.facade.utils import AWSFacadeUtils
from ScoutSuite.providers.utils import run_concurrently


class EC2Facade:
    async def get_instance_user_data(self, region: str, instance_id: str):
        ec2_client = await AWSFacadeUtils.get_client('ec2', region)
        user_data_response = await run_concurrently(
            lambda: ec2_client.describe_instance_attribute(Attribute='userData', InstanceId=instance_id))

        if 'Value' not in user_data_response['UserData'].keys():
            return None

        return base64.b64decode(user_data_response['UserData']['Value']).decode('utf-8')

    async def get_instances(self, region, vpc):
        filters = [{'Name': 'vpc-id', 'Values': [vpc]}]
        reservations =\
            await AWSFacadeUtils.get_all_pages('ec2', region, 'describe_instances', 'Reservations', Filters=filters)

        instances = []
        for reservation in reservations:
            for instance in reservation['Instances']:
                instance['ReservationId'] = reservation['ReservationId']
                instances.append(instance)
                
        return instances

    async def get_security_groups(self, region, vpc):
        filters = [{'Name': 'vpc-id', 'Values': [vpc]}]
        return await AWSFacadeUtils.get_all_pages(
            'ec2', region, 'describe_security_groups', 'SecurityGroups', Filters=filters)

    async def get_vpcs(self, region):
        ec2_client = await run_concurrently(lambda: boto3.client('ec2', region_name=region))
        return await run_concurrently(lambda: ec2_client.describe_vpcs()['Vpcs'])

    async def get_images(self, region, owner_id):
        filters = [{'Name': 'owner-id', 'Values': [owner_id]}]
        client = await AWSFacadeUtils.get_client('ec2', region)
        response = await run_concurrently(lambda: client.describe_images(Filters=filters))

        return response['Images']

    async def get_network_interfaces(self, region, vpc):
        filters = [{'Name': 'vpc-id', 'Values': [vpc]}]
        return await AWSFacadeUtils.get_all_pages(
            'ec2', region, 'describe_network_interfaces', 'NetworkInterfaces', Filters=filters)

    async def get_volumes(self, region):
        return await AWSFacadeUtils.get_all_pages('ec2', region, 'describe_volumes', 'Volumes')

    async def get_snapshots(self, region, owner_id):
        filters = [{'Name': 'owner-id', 'Values': [owner_id]}]
        snapshots = await AWSFacadeUtils.get_all_pages(
            'ec2', region, 'describe_snapshots', 'Snapshots', Filters=filters)

        ec2_client = await AWSFacadeUtils.get_client('ec2', region)
        for snapshot in snapshots:
            snapshot['CreateVolumePermissions'] = await run_concurrently(lambda: ec2_client.describe_snapshot_attribute(
                Attribute='createVolumePermission',
                SnapshotId=snapshot['SnapshotId'])['CreateVolumePermissions'])

        return snapshots
