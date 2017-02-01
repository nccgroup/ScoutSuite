from AWSScout2.utils_cloudtrail import CloudTrailConfig
from AWSScout2.utils_iam import IAMConfig
from AWSScout2.utils_redshift import RedshiftConfig
from AWSScout2.utils_sns import SNSConfig
from AWSScout2.utils_sqs import SQSConfig

class ServicesConfig(object):
    """
    Object that holds the necessary AWS configuration for all services in scope.

    :ivar cloudtrail: CloudTrail configuration
    :ivar cloudwatch: CloudWatch configuration
    :ivar ec2: EC2 configuration
    :ivar iam: IAM configuration
    :ivar rds: RDS configuration
    """

    def __init__(self):
        self.cloudtrail = CloudTrailConfig()
        self.cloudwatch = None
        self.ec2 = None
#        self.iam = IAMConfig()
        self.redshift = RedshiftConfig()
        self.rds = None
        self.s3 = None
        self.ses = None
        self.sns = SNSConfig()
        self.sqs = SQSConfig()
