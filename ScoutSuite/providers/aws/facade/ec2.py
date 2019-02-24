import boto3
import base64
import itertools

from ScoutSuite.providers.aws.facade.utils import AWSFacadeUtils


class EC2Facade:
    def get_instance_user_data(self, region, instance_id):
        # TODO: We should save a list of the clients by region, as they are created.
        ec2_client = boto3.client('ec2', region_name=region)
        user_data_response = ec2_client.describe_instance_attribute(
            Attribute='userData', InstanceId=instance_id)

        if 'Value' not in user_data_response['UserData'].keys():
            return None

        return base64.b64decode(user_data_response['UserData']['Value']).decode('utf-8')

    def get_instances(self, region, vpc):
        ec2_client = boto3.client('ec2', region_name=region)

        return AWSFacadeUtils.get_all_pages(
            lambda: ec2_client.describe_instances(Filters=[{'Name': 'vpc-id', 'Values': [vpc]}]),
            lambda response: itertools.chain.from_iterable(
                [reservation['Instances'] for reservation in response['Reservations']])
        )

    def get_security_groups(self, region, vpc):
        ec2_client = boto3.client('ec2', region_name=region)

        return AWSFacadeUtils.get_all_pages(
            lambda: ec2_client.describe_security_groups(Filters=[{'Name': 'vpc-id', 'Values': [vpc]}]),
            lambda response: response['SecurityGroups']
        )

    def get_vpcs(self, region):
        ec2_client  = boto3.client('ec2', region_name=region)
        return AWSFacadeUtils.get_all_pages(
            lambda: ec2_client.describe_vpcs(),
            lambda response: response['Vpcs']
        )

    def get_images(self, region, owner_id):
        ec2_client = boto3.client('ec2', region_name=region)
        return AWSFacadeUtils.get_all_pages(
            lambda: ec2_client .describe_images(Filters=[{'Name': 'owner-id', 'Values': [owner_id]}]),
            lambda response: response['Images']
        )

    def get_volumes(self, region):
        ec2_client = boto3.client('ec2', region_name=region)
        return AWSFacadeUtils.get_all_pages(
            lambda: ec2_client.describe_volumes(),
            lambda response: response['Volumes']
        )


    def get_snapshots(self, region, owner_id):
        ec2_client = boto3.client('ec2', region_name=region)
        snapshots = AWSFacadeUtils.get_all_pages(
            lambda: ec2_client.describe_snapshots(Filters=[{'Name': 'owner-id', 'Values': [owner_id]}]),
            lambda response: response['Snapshots']
        )

        for snapshot in snapshots:
            snapshot['CreateVolumePermissions'] = ec2_client.describe_snapshot_attribute(
                Attribute='createVolumePermission', 
                SnapshotId=snapshot['SnapshotId'])['CreateVolumePermissions']

        return snapshots

            