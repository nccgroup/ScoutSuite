# -*- coding: utf-8 -*-

from opinel.utils.console import printError, printException, printInfo

from AWSScout2.utils import format_service_name
from AWSScout2.services.cloudformation import CloudFormationConfig
from AWSScout2.services.cloudtrail import CloudTrailConfig
from AWSScout2.services.cloudwatch import CloudWatchConfig
from AWSScout2.services.directconnect import DirectConnectConfig
from AWSScout2.services.ec2 import EC2Config
from AWSScout2.services.efs import EFSConfig
from AWSScout2.services.elasticache import ElastiCacheConfig
from AWSScout2.services.elb import ELBConfig
from AWSScout2.services.elbv2 import ELBv2Config
from AWSScout2.services.emr import EMRConfig
from AWSScout2.services.iam import IAMConfig
from AWSScout2.services.awslambda import LambdaConfig
from AWSScout2.services.rds import RDSConfig
from AWSScout2.services.redshift import RedshiftConfig
from AWSScout2.services.route53 import Route53Config, Route53DomainsConfig
from AWSScout2.services.s3 import S3Config
from AWSScout2.services.ses import SESConfig
from AWSScout2.services.sns import SNSConfig
from AWSScout2.services.sqs import SQSConfig
from AWSScout2.services.vpc import VPCConfig


class ServicesConfig(object):
    """
    Object that holds the necessary AWS configuration for all services in scope.
                                        
    :ivar cloudtrail:                   CloudTrail configuration
    :ivar cloudwatch:                   CloudWatch configuration: TODO
    :ivar ec2:                          EC2 configuration
    :ivar iam:                          IAM configuration
    :ivar rds:                          RDS configuration
    :ivar redshift:                     Redshift configuration
    :ivar s3:                           S3 configuration
    :ivar ses:                          SES configuration: TODO
    "ivar sns:                          SNS configuration
    :ivar sqs:                          SQS configuration
    """

    def __init__(self, metadata, thread_config = 4):

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


    def fetch(self, credentials, services = [], regions = [], partition_name = ''):
        """

        :param credentials:
        :param services:
        :param regions:
        :param partition_name:
        :return:
        """
        for service in vars(self):
            try:
                if services != [] and service not in services:
                    continue
                service_config = getattr(self, service)
                if 'fetch_all' in dir(service_config):
                    method_args = {}
                    method_args['credentials'] = credentials
                    if service != 'iam':
                        method_args['regions'] = regions
                        method_args['partition_name'] = partition_name
                    service_config.fetch_all(**method_args)
                    if hasattr(service_config, 'finalize'):
                        service_config.finalize()
            except Exception as e:
                printError('Error: could not fetch %s configuration.' % service)
                printException(e)

    def single_service_pass(self):
        pass

    def multi_service_pass(self):
        pass





def postprocessing(aws_config):
    for service in aws_config['services']:
        method_name = '%s_postprocessing' % service
        if method_name in globals():
            try:
                printInfo('Post-processing %s config...' % format_service_name(service))
                method = globals()[method_name]
                method(aws_config)
            except Exception as e:
                printException(e)
                pass



