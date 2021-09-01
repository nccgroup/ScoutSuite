from boto3.session import Session

from ScoutSuite.providers.aws.facade.acm import AcmFacade
from ScoutSuite.providers.aws.facade.awslambda import LambdaFacade
from ScoutSuite.providers.aws.facade.basefacade import AWSBaseFacade
from ScoutSuite.providers.aws.facade.cloudformation import CloudFormation
from ScoutSuite.providers.aws.facade.cloudtrail import CloudTrailFacade
from ScoutSuite.providers.aws.facade.cloudwatch import CloudWatch
from ScoutSuite.providers.aws.facade.cloudfront import CloudFront
from ScoutSuite.providers.aws.facade.codebuild import CodeBuild
from ScoutSuite.providers.aws.facade.config import ConfigFacade
from ScoutSuite.providers.aws.facade.directconnect import DirectConnectFacade
from ScoutSuite.providers.aws.facade.dynamodb import DynamoDBFacade
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
from ScoutSuite.providers.aws.utils import get_aws_account_id, get_partition_name
from ScoutSuite.providers.utils import run_concurrently

from ScoutSuite.core.conditions import print_error

# Try to import proprietary facades
try:
    from ScoutSuite.providers.aws.facade.cognito_private import CognitoFacade
except ImportError:
    pass
try:
    from ScoutSuite.providers.aws.facade.docdb_private import DocDBFacade
except ImportError:
    pass
try:
    from ScoutSuite.providers.aws.facade.ecs_private import ECSFacade
except ImportError:
    pass
try:
    from ScoutSuite.providers.aws.facade.ecr_private import ECRFacade
except ImportError:
    pass
try:
    from ScoutSuite.providers.aws.facade.eks_private import EKSFacade
except ImportError:
    pass
try:
    from ScoutSuite.providers.aws.facade.guardduty_private import GuardDutyFacade
except ImportError:
    pass
try:
    from ScoutSuite.providers.aws.facade.ssm_private import SSMFacade
except ImportError:
    pass


class AWSFacade(AWSBaseFacade):
    def __init__(self, credentials=None):
        super().__init__()
        self.owner_id = get_aws_account_id(credentials.session)
        self.partition = get_partition_name(credentials.session)
        self.session = credentials.session
        self._instantiate_facades()

    async def build_region_list(self, service: str, chosen_regions=None, excluded_regions=None, partition_name='aws'):

        available_services = None
        try:
            available_services = await run_concurrently(
                lambda: Session(region_name='us-east-1').get_available_services())
        except Exception as e:
            # see https://github.com/nccgroup/ScoutSuite/issues/548
            # If failed with the us-east-1 region, we'll try to use the region from the profile
            try:
                available_services = await run_concurrently(
                    lambda: Session(region_name=self.session.region_name).get_available_services())
            except Exception as e:
                # see https://github.com/nccgroup/ScoutSuite/issues/685
                # If above failed, and regions were explicitly specified, will try with those until one works
                if chosen_regions:
                    for region in chosen_regions:
                        try:
                            available_services = await run_concurrently(
                                lambda: Session(region_name=region).get_available_services())
                            break
                        except Exception as e:
                            exception = e
                    if not available_services:
                        raise exception
                else:
                    raise e

        if service not in available_services:
            # the cognito service is a composition of two boto3 services
            if service == "cognito":
                if "cognito-idp" not in available_services:
                    raise Exception('Service cognito-idp is not available.')
                elif "cognito-identity" not in available_services:
                    raise Exception('Service cognito-identity is not available.')
            else:
                raise Exception('Service ' + service + ' is not available.')

        regions = None
        try:
            # the cognito service is a composition of two boto3 services
            if service != "cognito":
                regions = await run_concurrently(
                    lambda: Session(region_name='us-east-1').get_available_regions(service,
                                                                                   partition_name))
            else:
                idp_regions = await run_concurrently(
                    lambda: Session(region_name='us-east-1').get_available_regions("cognito-idp",
                                                                                   partition_name))
                identity_regions = await run_concurrently(
                    lambda: Session(region_name='us-east-1').get_available_regions("cognito-identity",
                                                                                   partition_name))
                regions = [value for value in idp_regions if value in identity_regions]
        except Exception as e:
            # see https://github.com/nccgroup/ScoutSuite/issues/548
            # If failed with the us-east-1 region, we'll try to use the region from the profile
            try:
                # the cognito service is a composition of two boto3 services
                if service != "cognito":
                    regions = await run_concurrently(
                        lambda: Session(region_name=self.session.region_name).get_available_regions(service,
                                                                                                    partition_name))
                else:
                    idp_regions = await run_concurrently(
                        lambda: Session(region_name=self.session.region_name).get_available_regions("cognito-idp",
                                                                                                    partition_name))
                    identity_regions = await run_concurrently(
                        lambda: Session(region_name=self.session.region_name).get_available_regions("cognito-identity",
                                                                                                    partition_name))
                    regions = [value for value in idp_regions if value in identity_regions]
            except Exception as e:
                # see https://github.com/nccgroup/ScoutSuite/issues/685
                # If above failed, and regions were explicitly specified, will try with those until one works
                if chosen_regions:
                    for region in chosen_regions:
                        try:
                            # the cognito service is a composition of two boto3 services
                            if service != "cognito":
                                regions = await run_concurrently(
                                    lambda: Session(region_name=region).get_available_regions(service,
                                                                                              partition_name))
                            else:
                                idp_regions = await run_concurrently(
                                    lambda: Session(region_name=region).get_available_regions(
                                        "cognito-idp",
                                        partition_name))
                                identity_regions = await run_concurrently(
                                    lambda: Session(region_name=region).get_available_regions(
                                        "cognito-identity",
                                        partition_name))
                                regions = [value for value in idp_regions if value in identity_regions]
                            break
                        except Exception as e:
                            exception = e
                    if not regions:
                        raise exception
                else:
                    raise e

        if not regions:
            # Could be an instance of https://github.com/boto/boto3/issues/1662
            if service == 'eks':  # TODO fix when the issue is resolved
                regions = ['ap-east-1',
                           'ap-northeast-1',
                           'ap-northeast-2',
                           'ap-south-1',
                           'ap-southeast-1',
                           'ap-southeast-2',
                           'ca-central-1',
                           'eu-central-1',
                           'eu-north-1',
                           'eu-west-1',
                           'eu-west-2',
                           'eu-west-3',
                           'me-south-1',
                           'sa-east-1',
                           'us-east-1',
                           'us-east-2',
                           # 'us-west-1',
                           'us-west-2']
            else:
                print_error('"get_available_regions" returned an empty array for service "{}", '
                            'something is wrong'.format(service))

        # identify regions that are not opted-in
        ec2_not_opted_in_regions = None
        try:
            ec2_not_opted_in_regions = self.session.client('ec2', 'us-east-1') \
                .describe_regions(AllRegions=True, Filters=[{'Name': 'opt-in-status', 'Values': ['not-opted-in']}])
        except Exception as e:
            # see https://github.com/nccgroup/ScoutSuite/issues/548
            # If failed with the us-east-1 region, we'll try to use the region from the profile
            try:
                ec2_not_opted_in_regions = \
                    self.session.client('ec2', self.session.region_name). \
                        describe_regions(AllRegions=True,
                                         Filters=[{'Name': 'opt-in-status',
                                                   'Values': ['not-opted-in']}])
            except Exception as e:
                # see https://github.com/nccgroup/ScoutSuite/issues/685
                # If above failed, and regions were explicitly specified, will try with those until
                # one works
                if chosen_regions:
                    for region in chosen_regions:
                        try:
                            ec2_not_opted_in_regions = self.session.client('ec2', region).describe_regions(
                                AllRegions=True,
                                Filters=[{'Name': 'opt-in-status',
                                          'Values': ['not-opted-in']}])
                            break
                        except Exception as e:
                            exception = e
                    if not ec2_not_opted_in_regions:
                        raise exception
                else:
                    raise e

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
        self.dynamodb = DynamoDBFacade(self.session)
        self.efs = EFSFacade(self.session)
        self.elasticache = ElastiCacheFacade(self.session)
        self.route53 = Route53Facade(self.session)
        self.cloudfront = CloudFront(self.session)
        self.codebuild = CodeBuild(self.session)
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
        self.emr = EMRFacade(self.session)

        # Instantiate facades for proprietary services
        try:
            self.cognito = CognitoFacade(self.session)
        except NameError:
            pass
        try:
            self.docdb = DocDBFacade(self.session)
        except NameError:
            pass
        try:
            self.ecs = ECSFacade(self.session)
        except NameError:
            pass
        try:
            self.ecr = ECRFacade(self.session)
        except NameError:
            pass
        try:
            self.eks = EKSFacade(self.session)
        except NameError:
            pass
        try:
            self.guardduty = GuardDutyFacade(self.session)
        except NameError:
            pass
        try:
            self.ssm = SSMFacade(self.session)
        except NameError:
            pass
