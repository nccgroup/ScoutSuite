from ScoutSuite.providers.aws.facade import AWSFacade
from ScoutSuite.providers.aws.resources.awslambda import Lambdas
from ScoutSuite.providers.aws.resources.cloudformation import CloudFormation
from ScoutSuite.providers.aws.resources.cloudtrail import CloudTrail
from ScoutSuite.providers.aws.resources.cloudwatch import CloudWatch
from ScoutSuite.providers.aws.resources.directconnect import DirectConnect
from ScoutSuite.providers.aws.resources.ec2 import EC2
from ScoutSuite.providers.aws.resources.efs import EFS
from ScoutSuite.providers.aws.resources.elasticache import ElastiCache
from ScoutSuite.providers.aws.resources.elb import ELB
from ScoutSuite.providers.aws.resources.elbv2 import ELBv2
from ScoutSuite.providers.aws.resources.emr import EMR
from ScoutSuite.providers.aws.resources.iam import IAM
from ScoutSuite.providers.aws.resources.rds import RDS
from ScoutSuite.providers.aws.resources.redshift import Redshift
from ScoutSuite.providers.aws.resources.route53 import Route53
from ScoutSuite.providers.aws.resources.s3 import S3
from ScoutSuite.providers.aws.resources.ses import SES
from ScoutSuite.providers.aws.resources.sns import SNS
from ScoutSuite.providers.aws.resources.sqs import SQS
from ScoutSuite.providers.aws.resources.vpc import VPC
from ScoutSuite.providers.base.configs.services import BaseServicesConfig

# Try to import proprietary services
try:
    from ScoutSuite.providers.aws.resources.private_dynamodb import DynamoDB
except ImportError:
    pass
try:
    from ScoutSuite.providers.aws.resources.private_config import Config
except ImportError:
    pass
try:
    from ScoutSuite.providers.aws.resources.private_kms import KMS
except ImportError:
    pass


class AWSServicesConfig(BaseServicesConfig):
    """
    Object that holds the necessary AWS configuration for all services in scope.

    :ivar cloudtrail:                   CloudTrail configuration
    :ivar cloudwatch:                   CloudWatch configuration:
    :ivar config:                       Config configuration
    :ivar dynamodb:                     DynomaDB configuration
    :ivar ec2:                          EC2 configuration
    :ivar iam:                          IAM configuration
    :ivar kms:                          KMS configuration
    :ivar rds:                          RDS configuration
    :ivar redshift:                     Redshift configuration
    :ivar s3:                           S3 configuration
    :ivar ses:                          SES configuration:
    "ivar sns:                          SNS configuration
    :ivar sqs:                          SQS configuration
    """

    def __init__(self, credentials=None, **kwargs):
        super(AWSServicesConfig, self).__init__(credentials)

        facade = AWSFacade(credentials)

        self.cloudwatch = CloudWatch(facade)
        self.cloudformation = CloudFormation(facade)
        self.cloudtrail = CloudTrail(facade)
        self.directconnect = DirectConnect(facade)
        self.ec2 = EC2(facade)
        self.efs = EFS(facade)
        self.elasticache = ElastiCache(facade)
        self.iam = IAM(facade)
        self.elb = ELB(facade)
        self.elbv2 = ELBv2(facade)
        self.emr = EMR(facade)
        self.awslambda = Lambdas(facade)
        self.route53 = Route53(facade)
        self.redshift = Redshift(facade)
        self.s3 = S3(facade)
        self.rds = RDS(facade)
        self.vpc = VPC(facade)
        self.sqs = SQS(facade)
        self.ses = SES(facade)
        self.sns = SNS(facade)

        try:
            self.dynamodb = DynamoDB(facade)
        except NameError as _:
            pass
        try:
            self.config = Config(facade)
        except NameError as _:
            pass
        try:
            self.kms = KMS(facade)
        except NameError as _:
            pass

    def _is_provider(self, provider_name):
        return provider_name == 'aws'
