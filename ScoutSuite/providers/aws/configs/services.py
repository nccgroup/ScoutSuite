# -*- coding: utf-8 -*-

from ScoutSuite.providers.aws.resources.awslambda.service import Lambdas
from ScoutSuite.providers.aws.resources.cloudwatch.service import CloudWatch
from ScoutSuite.providers.aws.resources.cloudformation.service import CloudFormation
from ScoutSuite.providers.aws.resources.cloudtrail.service import CloudTrail
from ScoutSuite.providers.aws.resources.directconnect.service import DirectConnect
from ScoutSuite.providers.aws.resources.ec2.service import EC2
from ScoutSuite.providers.aws.resources.efs.service import EFS
from ScoutSuite.providers.aws.resources.elasticache.service import ElastiCache
from ScoutSuite.providers.aws.services.elb import ELBConfig
from ScoutSuite.providers.aws.resources.elbv2.service import ELBv2
from ScoutSuite.providers.aws.resources.emr.service import EMR
from ScoutSuite.providers.aws.services.iam import IAMConfig
from ScoutSuite.providers.aws.services.rds import RDSConfig
from ScoutSuite.providers.aws.resources.redshift.service import Redshift
from ScoutSuite.providers.aws.services.route53 import Route53Config, Route53DomainsConfig
from ScoutSuite.providers.aws.services.s3 import S3Config
from ScoutSuite.providers.aws.services.ses import SESConfig
from ScoutSuite.providers.aws.services.sns import SNSConfig
from ScoutSuite.providers.aws.services.sqs import SQSConfig
from ScoutSuite.providers.aws.services.vpc import VPCConfig
from ScoutSuite.providers.base.configs.services import BaseServicesConfig

try:
    from ScoutSuite.providers.aws.resources.dynamodb.service_private import DynamoDB
    from ScoutSuite.providers.aws.resources.config.service_private import Config
    from ScoutSuite.providers.aws.services.kms_private import KMSConfig
except ImportError:
    Config = None
    DynamoDB = None
    KMSConfig = None


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
    :ivar ses:                          SES configuration: TODO
    "ivar sns:                          SNS configuration
    :ivar sqs:                          SQS configuration
    """

    def __init__(self, metadata=None, thread_config=4, **kwargs):

        super(AWSServicesConfig, self).__init__(metadata, thread_config)
        self.cloudwatch = CloudWatch()
        self.cloudformation = CloudFormation()
        self.cloudtrail = CloudTrail()
        self.directconnect = DirectConnect()
        self.ec2 = EC2()
        self.efs = EFS()
        self.elasticache = ElastiCache()
        self.elb = ELBConfig(metadata['compute']['elb'], thread_config)
        self.elbv2 = ELBv2()
        self.emr = EMR()
        self.iam = IAMConfig(thread_config)
        self.awslambda = Lambdas()
        self.redshift = Redshift()
        self.rds = RDSConfig(metadata['database']['rds'], thread_config)
        self.route53 = Route53Config(thread_config)
        self.route53domains = Route53DomainsConfig(thread_config)
        self.s3 = S3Config(thread_config)
        self.ses = SESConfig(metadata['messaging']['ses'], thread_config)
        self.sns = SNSConfig(metadata['messaging']['sns'], thread_config)
        self.sqs = SQSConfig(metadata['messaging']['sqs'], thread_config)
        self.vpc = VPCConfig(metadata['network']['vpc'], thread_config)

        try:
            self.dynamodb = DynamoDB()
            self.config = Config()
            self.kms = KMSConfig(metadata['security']['kms'], thread_config)
        except (NameError, TypeError):
            pass

    def _is_provider(self, provider_name):
        return provider_name == 'aws'
