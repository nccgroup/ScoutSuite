import boto3
from botocore.session import Session
from collections import Counter
import itertools
import base64

# TODO: It would be interesting to split the facade in different sub-facades. For example, a call could look like this:
#       facade.ec2.get_instances(region) or
#       facade.lambda.get_functions(region)


class AWSFacade(object):
    async def build_region_list(self, service, chosen_regions=None, partition_name='aws'):
        service = 'ec2containerservice' if service == 'ecs' else service
        available_services = Session().get_available_services()

        if service not in available_services:
            raise Exception('Service ' + service + ' is not available.')

        regions = Session().get_available_regions(service, partition_name)

        if chosen_regions:
            return list((Counter(regions) & Counter(chosen_regions)).elements())
        else:
            return regions

    def get_lambda_functions(self, region):
        aws_lambda = boto3.client('lambda', region_name=region)
        return self._get_all_pages(
            lambda: aws_lambda.list_functions(),
            lambda response: response['Functions']
        )

    def get_ec2_instances(self, region, vpc):
        ec2_client = boto3.client('ec2', region_name=region)

        return self._get_all_pages(
            lambda: ec2_client.describe_instances(Filters=[{'Name': 'vpc-id', 'Values': [vpc]}]),
            lambda response: itertools.chain.from_iterable(
                [reservation['Instances'] for reservation in response['Reservations']])
        )

    def get_vpcs(self, region):
        vpc_client = boto3.client('ec2', region_name=region)
        return self._get_all_pages(
            lambda: vpc_client.describe_vpcs(),
            lambda response: response['Vpcs']
        )

    def get_ec2_images(self, region, owner_id):
        vpc_client = boto3.client('ec2', region_name=region)
        return self._get_all_pages(
            lambda: vpc_client.describe_images(Filters=[{'Name': 'owner-id', 'Values': [owner_id]}]),
            lambda response: response['Images']
        )

    def _get_all_pages(self, api_call, parse_response):
        resources = []

        while True:
            response = api_call()

            resources.extend(parse_response(response))
            marker = response.get('NextMarker', None)
            if marker is None:
                break
        return resources

    def get_ec2_instance_user_data(self, region, instance_id):
        ec2_client = boto3.client('ec2', region_name=region)
        user_data_response = ec2_client.describe_instance_attribute(
            Attribute='userData', InstanceId=instance_id)

        if 'Value' not in user_data_response['UserData'].keys():
            return None

        return base64.b64decode(user_data_response['UserData']['Value']).decode('utf-8')
