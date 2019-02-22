import boto3
import base64
import itertools

from ScoutSuite.providers.aws.facade.utils import AWSFacadeUtils


class EC2Facade:
    def get_instance_user_data(self, region, instance_id):
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

    def get_vpcs(self, region):
        vpc_client = boto3.client('ec2', region_name=region)
        return AWSFacadeUtils.get_all_pages(
            lambda: vpc_client.describe_vpcs(),
            lambda response: response['Vpcs']
        )

    def get_images(self, region, owner_id):
        vpc_client = boto3.client('ec2', region_name=region)
        return AWSFacadeUtils.get_all_pages(
            lambda: vpc_client.describe_images(Filters=[{'Name': 'owner-id', 'Values': [owner_id]}]),
            lambda response: response['Images']
        )