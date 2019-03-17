from collections import Counter
from botocore.session import Session
import boto3

from ScoutSuite.providers.aws.facade.awslambda import LambdaFacade
from ScoutSuite.providers.aws.facade.cloudformation import CloudFormation
from ScoutSuite.providers.aws.facade.cloudtrail import CloudTrailFacade
from ScoutSuite.providers.aws.facade.cloudwatch import CloudWatch
from ScoutSuite.providers.aws.facade.directconnect import DirectConnectFacade
from ScoutSuite.providers.aws.facade.ec2 import EC2Facade
from ScoutSuite.providers.aws.facade.efs import EFSFacade
from ScoutSuite.providers.aws.facade.elasticache import ElastiCacheFacade
from ScoutSuite.providers.aws.facade.emr import EMRFacade
from ScoutSuite.providers.aws.facade.elbv2 import ELBv2Facade
from ScoutSuite.providers.aws.facade.basefacade import AWSBaseFacade
from ScoutSuite.providers.utils import run_concurrently


class AWSFacade(AWSBaseFacade):
    def __init__(self, credentials: dict = None):
        self._set_session(credentials)

        self.ec2 = EC2Facade(self.session)
        self.awslambda = LambdaFacade(self.session)
        self.cloudformation = CloudFormation(self.session)
        self.cloudtrail = CloudTrailFacade(self.session)
        self.cloudwatch = CloudWatch(self.session)
        self.directconnect = DirectConnectFacade(self.session)
        self.efs = EFSFacade(self.session)
        self.elasticache = ElastiCacheFacade(self.session)
        self.emr = EMRFacade(self.session)
        self.elbv2 = ELBv2Facade(self.session)

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

    def _set_session(self, credentials: dict):
        # TODO: This conditional check is ok for now, but eventually, the credentials should always be provided.
        if not credentials:
            self.session = None
            return

        session_params = {'aws_access_key_id': credentials.get('access_key'),
                          'aws_secret_access_key': credentials.get('secret_key'),
                          'aws_session_token': credentials.get('token')}

        self.session = boto3.session.Session(**session_params)

        # TODO: This should only be done in the constructor. I put this here for now, because this method is currently
        # called from outside, but it should not happen.
        self.ec2 = EC2Facade(self.session)
        self.awslambda = LambdaFacade(self.session)
        self.cloudformation = CloudFormation(self.session)
        self.cloudtrail = CloudTrailFacade(self.session)
        self.cloudwatch = CloudWatch(self.session)
        self.directconnect = DirectConnectFacade(self.session)
        self.efs = EFSFacade(self.session)
        self.elasticache = ElastiCacheFacade(self.session)
        self.emr = EMRFacade(self.session)
        self.elbv2 = ELBv2Facade(self.session)
