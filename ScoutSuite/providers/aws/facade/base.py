from boto3.session import Session

from ScoutSuite.providers.aws.facade.acm import AcmFacade
from ScoutSuite.providers.aws.facade.awslambda import LambdaFacade
from ScoutSuite.providers.aws.facade.basefacade import AWSBaseFacade
from ScoutSuite.providers.aws.facade.cloudformation import CloudFormation
from ScoutSuite.providers.aws.facade.cloudtrail import CloudTrailFacade
from ScoutSuite.providers.aws.facade.cloudwatch import CloudWatch
from ScoutSuite.providers.aws.facade.config import ConfigFacade
from ScoutSuite.providers.aws.facade.directconnect import DirectConnectFacade
from ScoutSuite.providers.aws.facade.ec2 import EC2Facade
from ScoutSuite.providers.aws.facade.efs import EFSFacade
from ScoutSuite.providers.aws.facade.elasticache import ElastiCacheFacade
from ScoutSuite.providers.aws.facade.elb import ELBFacade
from ScoutSuite.providers.aws.facade.elbv2 import ELBv2Facade
from ScoutSuite.providers.aws.facade.emr import EMRFacade
from ScoutSuite.providers.aws.facade.iam import IAMFacade
from ScoutSuite.providers.aws.facade.kms import KMSFacade
from ScoutSuite.providers.aws.facade.rds import RDSFacade
from ScoutSuite.providers.aws.facade.redshift import RedshiftFacade
from ScoutSuite.providers.aws.facade.route53 import Route53Facade
from ScoutSuite.providers.aws.facade.s3 import S3Facade
from ScoutSuite.providers.aws.facade.ses import SESFacade
from ScoutSuite.providers.aws.facade.sns import SNSFacade
from ScoutSuite.providers.aws.facade.sqs import SQSFacade
from ScoutSuite.providers.aws.facade.secretsmanager import SecretsManagerFacade
from ScoutSuite.providers.aws.utils import get_aws_account_id
from ScoutSuite.providers.utils import run_concurrently

# Try to import proprietary facades
try:
    from ScoutSuite.providers.aws.facade.dynamodb_private import DynamoDBFacade
except ImportError:
    pass


class AWSFacade(AWSBaseFacade):
    def __init__(self, credentials=None):
        super(AWSFacade, self).__init__()
        self.owner_id = get_aws_account_id(credentials.session)
        self.session = credentials.session
        self._instantiate_facades()

    async def build_region_list(self, service: str, chosen_regions=None, excluded_regions=None, partition_name='aws'):

        service = 'ec2containerservice' if service == 'ecs' else service
        available_services = await run_concurrently(lambda: Session(region_name='eu-west-1').get_available_services())

        if service not in available_services:
            raise Exception('Service ' + service + ' is not available.')

        regions = await run_concurrently(lambda: Session(region_name='eu-west-1').get_available_regions(service,
                                                                                                        partition_name))

        # identify regions that are not opted-in
        ec2_not_opted_in_regions = self.session.client('ec2', 'eu-west-1')\
            .describe_regions(AllRegions=True, Filters=[{'Name': 'opt-in-status', 'Values': ['not-opted-in']}])

        not_opted_in_regions = []
        if ec2_not_opted_in_regions['Regions']:
            for r in ec2_not_opted_in_regions['Regions']:
                not_opted_in_regions.append(r['RegionName'])

        # include specific regions
        if chosen_regions:
            regions = [r for r in regions if r in chosen_regions]
        # exclude specific regions
        if excluded_regions:
            regions = [r for r in regions if r not in excluded_regions]
        # exclude not opted in regions
        if not_opted_in_regions:
            regions = [r for r in regions if r not in not_opted_in_regions]

        return regions

    def _instantiate_facades(self):
        self.ec2 = EC2Facade(self.session, self.owner_id)
        self.acm = AcmFacade(self.session)
        self.awslambda = LambdaFacade(self.session)
        self.cloudformation = CloudFormation(self.session)
        self.cloudtrail = CloudTrailFacade(self.session)
        self.cloudwatch = CloudWatch(self.session)
        self.config = ConfigFacade(self.session)
        self.directconnect = DirectConnectFacade(self.session)
        self.efs = EFSFacade(self.session)
        self.elasticache = ElastiCacheFacade(self.session)
        self.emr = EMRFacade(self.session)
        self.route53 = Route53Facade(self.session)
        self.elb = ELBFacade(self.session)
        self.elbv2 = ELBv2Facade(self.session)
        self.iam = IAMFacade(self.session)
        self.kms = KMSFacade(self.session)
        self.rds = RDSFacade(self.session)
        self.redshift = RedshiftFacade(self.session)
        self.s3 = S3Facade(self.session)
        self.ses = SESFacade(self.session)
        self.sns = SNSFacade(self.session)
        self.sqs = SQSFacade(self.session)
        self.secretsmanager = SecretsManagerFacade(self.session)

        # Instantiate facades for proprietary services
        try:
            self.dynamodb = DynamoDBFacade(self.session)
        except NameError:
            pass
