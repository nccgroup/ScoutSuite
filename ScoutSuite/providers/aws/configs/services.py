# -*- coding: utf-8 -*-

from ScoutSuite.providers.aws.resources.awslambda.service import Lambdas
from ScoutSuite.providers.aws.resources.cloudwatch.service import CloudWatch
from ScoutSuite.providers.aws.resources.cloudformation.service import CloudFormation
from ScoutSuite.providers.aws.resources.cloudtrail.service import CloudTrail
from ScoutSuite.providers.aws.resources.directconnect.service import DirectConnect
from ScoutSuite.providers.aws.resources.ec2.service import EC2
from ScoutSuite.providers.aws.resources.efs.service import EFS
from ScoutSuite.providers.aws.resources.elasticache.service import ElastiCache
from ScoutSuite.providers.aws.resources.elb.service import ELB
from ScoutSuite.providers.aws.resources.elbv2.service import ELBv2
from ScoutSuite.providers.aws.resources.iam.service import IAM
from ScoutSuite.providers.aws.resources.emr.service import EMR
from ScoutSuite.providers.aws.resources.route53.service import Route53
from ScoutSuite.providers.aws.resources.rds.service import RDS
from ScoutSuite.providers.aws.resources.redshift.service import Redshift
from ScoutSuite.providers.aws.resources.s3.service import S3
from ScoutSuite.providers.aws.resources.vpc.service import VPC
from ScoutSuite.providers.aws.resources.sqs.service import SQS
from ScoutSuite.providers.aws.resources.ses.service import SES
from ScoutSuite.providers.aws.resources.sns.service import SNS
from ScoutSuite.providers.base.configs.services import BaseServicesConfig
from ScoutSuite.providers.aws.facade.facade import AWSFacade

try:
    from ScoutSuite.providers.aws.resources.dynamodb.service_private import DynamoDB
    from ScoutSuite.providers.aws.resources.config.service_private import Config
    from ScoutSuite.providers.aws.resources.kms.service_private import KMS
except ImportError:
    DynamoDB = None
    Config = None
    KMS = None


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
            self.config = Config(facade)
            self.kms = KMS(facade)
        except (NameError, TypeError):
            pass

    def _is_provider(self, provider_name):
        return provider_name == 'aws'
