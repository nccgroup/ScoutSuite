from botocore.session import Session
from collections import Counter
from ScoutSuite.providers.aws.facade.ec2 import EC2Facade
from ScoutSuite.providers.aws.facade.awslambda import LambdaFacade

class AWSFacade(object):
    def __init__(self):
        self.ec2 = EC2Facade()
        self.awslambda = LambdaFacade()


    async def build_region_list(self, service: str, chosen_regions=None, partition_name='aws'):
        service = 'ec2containerservice' if service == 'ecs' else service
        available_services = Session().get_available_services()

        if service not in available_services:
            raise Exception('Service ' + service + ' is not available.')

        regions = Session().get_available_regions(service, partition_name)

        if chosen_regions:
            return list((Counter(regions) & Counter(chosen_regions)).elements())
        else:
            return regions