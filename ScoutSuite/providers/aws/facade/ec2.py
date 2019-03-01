import boto3
import base64
import itertools

from ScoutSuite.providers.aws.facade.utils import AWSFacadeUtils


class EC2Facade:
    def get_instance_user_data(self, region: str, instance_id: str):
        ec2_client = AWSFacadeUtils.get_client('ec2', region)
        user_data_response = ec2_client.describe_instance_attribute(Attribute='userData', InstanceId=instance_id)

        if 'Value' not in user_data_response['UserData'].keys():
            return None

        return base64.b64decode(user_data_response['UserData']['Value']).decode('utf-8')

    def get_instances(self, region, vpc):
        filters = [{'Name': 'vpc-id', 'Values': [vpc]}]
        reservations = AWSFacadeUtils.get_all_pages('ec2', region, 'describe_instances', 'Reservations', Filters=filters)
        return itertools.chain.from_iterable([reservation['Instances'] for reservation in reservations])

    def get_security_groups(self, region, vpc):
        filters = [{'Name': 'vpc-id', 'Values': [vpc]}]
        return AWSFacadeUtils.get_all_pages('ec2', region, 'describe_security_groups', 'SecurityGroups', Filters=filters)

    def get_vpcs(self, region):
        ec2_client = boto3.client('ec2', region_name=region)
        return ec2_client.describe_vpcs()['Vpcs']

    def get_images(self, region, owner_id):
        filters = [{'Name': 'owner-id', 'Values': [owner_id]}]
        response = AWSFacadeUtils.get_client('ec2', region) \
                                 .describe_images(Filters=filters)

        return response['Images']

    def get_network_interfaces(self, region, vpc):
        filters = [{'Name': 'vpc-id', 'Values': [vpc]}]
        return AWSFacadeUtils.get_all_pages('ec2', region, 'describe_network_interfaces', 'NetworkInterfaces', Filters=filters)

    def get_volumes(self, region):
        return AWSFacadeUtils.get_all_pages('ec2', region, 'describe_volumes', 'Volumes')

    def get_snapshots(self, region, owner_id):
        filters = [{'Name': 'owner-id', 'Values': [owner_id]}]
        snapshots = AWSFacadeUtils.get_all_pages('ec2', region, 'describe_snapshots', 'Snapshots', Filters=filters)

        ec2_client = AWSFacadeUtils.get_client('ec2', region)
        for snapshot in snapshots:
            snapshot['CreateVolumePermissions'] = ec2_client.describe_snapshot_attribute(
                Attribute='createVolumePermission',
                SnapshotId=snapshot['SnapshotId'])['CreateVolumePermissions']

        return snapshots
