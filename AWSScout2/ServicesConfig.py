from AWSScout2.utils_cloudtrail import CloudTrailConfig
from AWSScout2.utils_ec2 import EC2Config
from AWSScout2.utils_iam import IAMConfig
from AWSScout2.utils_rds import RDSConfig
from AWSScout2.utils_redshift import RedshiftConfig
from AWSScout2.utils_s3 import S3Config
from AWSScout2.utils_sns import SNSConfig
from AWSScout2.utils_sqs import SQSConfig
from AWSScout2.configs import formatted_service_name
from opinel.utils import printError, printException

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
        self.cloudtrail = CloudTrailConfig()
        self.cloudwatch = None
        self.ec2 = EC2Config()
        self.iam = IAMConfig()
        self.redshift = RedshiftConfig()
        self.rds = RDSConfig()
        self.s3 = S3Config()
        self.ses = None
        self.sns = SNSConfig()
        self.sqs = SQSConfig()


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
            except Exception as e:
                printError('Error: could not fetch %s configuration.' % service)
                printException(e)

    def single_service_pass(self):
        pass

    def multi_service_pass(self):
        pass

