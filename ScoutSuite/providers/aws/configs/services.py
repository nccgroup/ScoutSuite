# -*- coding: utf-8 -*-

from opinel.utils.console import printError, printException, printInfo, printDebug

from ScoutSuite.providers.aws.services.awslambda import LambdaConfig
from ScoutSuite.providers.aws.services.cloudformation import CloudFormationConfig
from ScoutSuite.providers.aws.services.cloudtrail import CloudTrailConfig
from ScoutSuite.providers.aws.services.cloudwatch import CloudWatchConfig
from ScoutSuite.providers.aws.services.directconnect import DirectConnectConfig
from ScoutSuite.providers.aws.services.ec2 import EC2Config
from ScoutSuite.providers.aws.services.efs import EFSConfig
from ScoutSuite.providers.aws.services.elasticache import ElastiCacheConfig
from ScoutSuite.providers.aws.services.elb import ELBConfig
from ScoutSuite.providers.aws.services.elbv2 import ELBv2Config
from ScoutSuite.providers.aws.services.emr import EMRConfig
from ScoutSuite.providers.aws.services.iam import IAMConfig
from ScoutSuite.providers.aws.services.kms import KMSConfig
from ScoutSuite.providers.aws.services.rds import RDSConfig
from ScoutSuite.providers.aws.services.redshift import RedshiftConfig
from ScoutSuite.providers.aws.services.route53 import Route53Config, Route53DomainsConfig
from ScoutSuite.providers.aws.services.s3 import S3Config
from ScoutSuite.providers.aws.services.ses import SESConfig
from ScoutSuite.providers.aws.services.sns import SNSConfig
from ScoutSuite.providers.aws.services.sqs import SQSConfig
from ScoutSuite.providers.aws.services.vpc import VPCConfig
from ScoutSuite.providers.base.configs.services import BaseServicesConfig
from ScoutSuite.utils import format_service_name

try:
    from ScoutSuite.providers.aws.services.dynamodb_private import DynamoDBConfig
except ImportError:
    pass


class AWSServicesConfig(BaseServicesConfig):
    """
    Object that holds the necessary AWS configuration for all services in scope.
                                        
    :ivar cloudtrail:                   CloudTrail configuration
    :ivar cloudwatch:                   CloudWatch configuration: TODO
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

        self.cloudformation = CloudFormationConfig(metadata['management']['cloudformation'], thread_config)
        self.cloudtrail = CloudTrailConfig(metadata['management']['cloudtrail'], thread_config)
        self.cloudwatch = CloudWatchConfig(metadata['management']['cloudwatch'], thread_config)
        self.directconnect = DirectConnectConfig(metadata['network']['directconnect'], thread_config)
        self.ec2 = EC2Config(metadata['compute']['ec2'], thread_config)
        self.efs = EFSConfig(metadata['storage']['efs'], thread_config)
        self.elasticache = ElastiCacheConfig(metadata['database']['elasticache'], thread_config)
        self.elb = ELBConfig(metadata['compute']['elb'], thread_config)
        self.elbv2 = ELBv2Config(metadata['compute']['elbv2'], thread_config)
        self.emr = EMRConfig(metadata['analytics']['emr'], thread_config)
        self.iam = IAMConfig(thread_config)
        self.kms = KMSConfig(metadata['security']['kms'], thread_config)
        self.awslambda = LambdaConfig(metadata['compute']['awslambda'], thread_config)
        self.redshift = RedshiftConfig(metadata['database']['redshift'], thread_config)
        self.rds = RDSConfig(metadata['database']['rds'], thread_config)
        self.route53 = Route53Config(thread_config)
        self.route53domains = Route53DomainsConfig(thread_config)
        self.s3 = S3Config(thread_config)
        self.ses = SESConfig(metadata['messaging']['ses'], thread_config)
        self.sns = SNSConfig(metadata['messaging']['sns'], thread_config)
        self.sqs = SQSConfig(metadata['messaging']['sqs'], thread_config)
        self.vpc = VPCConfig(metadata['network']['vpc'], thread_config)

        try:
            self.dynamodb = DynamoDBConfig(metadata['database']['dynamodb'], thread_config)
        except NameError as e:
            pass

    def _is_provider(self, provider_name):
        return provider_name == 'aws'

    # TODO is this ever called?
    # def single_service_pass(self):
    #     pass

    # TODO is this ever called?
    # def multi_service_pass(self):
    #     pass

    # TODO is this ever called?
    # def postprocessing(self):
    #     for service in self.services:
    #         method_name = '%s_postprocessing' % service
    #         if method_name in globals():
    #             try:
    #                 printInfo('Post-processing %s config...' % format_service_name(service))
    #                 method = globals()[method_name]
    #                 method(aws_config)
    #             except Exception as e:
    #                 printException(e)
    #                 pass
