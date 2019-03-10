from collections import Counter
from botocore.session import Session

from ScoutSuite.providers.aws.facade.awslambda import LambdaFacade
from ScoutSuite.providers.aws.facade.cloudformation import CloudFormation
from ScoutSuite.providers.aws.facade.cloudtrail import CloudTrailFacade
from ScoutSuite.providers.aws.facade.cloudwatch import CloudWatch
from ScoutSuite.providers.aws.facade.ec2 import EC2Facade
from ScoutSuite.providers.aws.facade.efs import EFSFacade
from ScoutSuite.providers.aws.facade.directconnect import DirectConnectFacade
from ScoutSuite.providers.utils import run_concurrently



class AWSFacade(object):

    def __init__(self):
        self.ec2 = EC2Facade()
        self.awslambda = LambdaFacade()
        self.cloudformation = CloudFormation()
        self.cloudtrail = CloudTrailFacade()
        self.cloudwatch = CloudWatch()
        self.directconnect = DirectConnectFacade()
        self.efs = EFSFacade()

    async def build_region_list(self, service: str, chosen_regions=None, partition_name='aws'):
        service = 'ec2containerservice' if service == 'ecs' else service
        available_services = await run_concurrently(lambda: Session().get_available_services())

        if service not in available_services:
            raise Exception('Service ' + service + ' is not available.')

        regions = await run_concurrently(lambda: Session().get_available_regions(service, partition_name))

        if chosen_regions:
            return list((Counter(regions) & Counter(chosen_regions)).elements())
        else:
            return regions
