from AWSScout2.utils_cloudtrail import CloudTrailConfig
from AWSScout2.utils_ec2 import EC2Config
from AWSScout2.utils_iam import IAMConfig
from AWSScout2.utils_rds import RDSConfig
from AWSScout2.utils_redshift import RedshiftConfig
from AWSScout2.utils_s3 import S3Config
from AWSScout2.utils_sns import SNSConfig
from AWSScout2.utils_sqs import SQSConfig

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
