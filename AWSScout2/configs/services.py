# -*- coding: utf-8 -*-

from opinel.utils.console import printError, printException, printInfo

from AWSScout2.utils import format_service_name
from AWSScout2.services.cloudformation import CloudFormationConfig
from AWSScout2.services.cloudtrail import CloudTrailConfig
from AWSScout2.services.ec2 import EC2Config
from AWSScout2.services.elb import ELBConfig
from AWSScout2.services.elbv2 import ELBv2Config
from AWSScout2.services.iam import IAMConfig
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

    def __init__(self):
        self.cloudformation = CloudFormationConfig()
        self.cloudtrail = CloudTrailConfig()
        #self.cloudwatch = None
        self.ec2 = EC2Config()
        self.elb = ELBConfig()
        self.elbv2 = ELBv2Config()
        self.iam = IAMConfig()
        self.redshift = RedshiftConfig()
        self.rds = RDSConfig()
        self.route53 = Route53Config()
        self.route53domains = Route53DomainsConfig()
        self.s3 = S3Config()
        self.ses = SESConfig()
        self.sns = SNSConfig()
        self.sqs = SQSConfig()
        self.vpc = VPCConfig()


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



