import boto3
import base64
import itertools

from ScoutSuite.providers.aws.facade.utils import AWSFacadeUtils


class EC2Facade:
    def get_instance_user_data(self, region: str, instance_id: str):
        # TODO: We should save a list of the clients by region, as they are created.
        ec2_client = boto3.client('ec2', region_name=region)
        user_data_response = ec2_client.describe_instance_attribute(Attribute='userData', InstanceId=instance_id)

        if 'Value' not in user_data_response['UserData'].keys():
            return None

        return base64.b64decode(user_data_response['UserData']['Value']).decode('utf-8')

    def get_instances(self, region, vpc):
        ec2_client = boto3.client('ec2', region_name=region)

        return AWSFacadeUtils.get_all_pages(
            lambda next_token: ec2_client.describe_instances(Filters=[{'Name': 'vpc-id', 'Values': [vpc]}], NextToken=next_token),
            lambda response: itertools.chain.from_iterable([reservation['Instances'] for reservation in response['Reservations']]),
            'NextToken'
        )

    def get_security_groups(self, region, vpc):
        ec2_client = boto3.client('ec2', region_name=region)
        filter = [{'Name': 'vpc-id', 'Values': [vpc]}]

        return AWSFacadeUtils.get_all_pages(
            lambda next_token: ec2_client.describe_security_groups(Filters=filter, NextToken=next_token),
            lambda response: response['SecurityGroups'],
            'NextToken'
        )

    def get_vpcs(self, region):
        ec2_client  = boto3.client('ec2', region_name=region)
        return ec2_client.describe_vpcs()['Vpcs']

    def get_images(self, region, owner_id):
        ec2_client = boto3.client('ec2', region_name=region)
        filter = [{'Name': 'owner-id', 'Values': [owner_id]}]
        return ec2_client.describe_images(Filters=filter)['Images']

    def get_network_interfaces(self, region, vpc):
        ec2_client = boto3.client('ec2', region_name=region)
        filter = [{'Name': 'vpc-id', 'Values': [vpc]}]

        return AWSFacadeUtils.get_all_pages(
            lambda next_token: ec2_client.describe_network_interfaces(Filters=filter, NextToken=next_token),
            lambda response: response['NetworkInterfaces'],
            'NextToken'
        )

    def get_volumes(self, region):
        ec2_client = boto3.client('ec2', region_name=region)
        return AWSFacadeUtils.get_all_pages(
            lambda next_token: ec2_client.describe_volumes(NextToken=next_token),
            lambda response: response['Volumes'],
            'NextToken'
        )


    def get_snapshots(self, region, owner_id):
        ec2_client = boto3.client('ec2', region_name=region)
        filter = [{'Name': 'owner-id', 'Values': [owner_id]}]
        snapshots = AWSFacadeUtils.get_all_pages(
            lambda next_token: ec2_client.describe_snapshots(Filters=filter, NextToken=next_token),
            lambda response: response['Snapshots'],
            'NextToken'
        )

        for snapshot in snapshots:
            snapshot['CreateVolumePermissions'] = ec2_client.describe_snapshot_attribute(
                Attribute='createVolumePermission', 
                SnapshotId=snapshot['SnapshotId'])['CreateVolumePermissions']

        return snapshots

            