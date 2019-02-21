import boto3
from botocore.session import Session
from collections import Counter

# TODO: Handle authentication better. I don't even know how it currently works. I think connect_service is called somewhere.
class AwsFacade(object):
    def get_lambda_functions(self, region):
        aws_lambda = boto3.client('lambda', region_name=region)
        
        functions = []
        
        while True:
            response = aws_lambda.list_functions()

            functions.extend(response['Functions'])
            marker = response.get('NextMarker', None)
            if marker is None:
                break

        return functions

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
