from AWSScout2.utils_cloudwatch import *

#
# Test for Scout2 CloudWatch functions
#
class TestScout2CloudWatchUtilsClass:

    configPrintException(True)

    #
    # Test get_cloudwatch_region in us-east-1
    #
    def test_get_cloudwatch_region(self):
        # TODO: change to us-east-1
        credentials = read_creds('default')
        service_config = {'regions': {'us-east-1': {}}}
        get_cloudwatch_region(params = {'region': 'us-east-1', 'creds': credentials, 'cloudwatch_config': service_config})

    # 
    # Test get_cloudwatch_info (multiple thread of get_cloudwatch_region)
    # 1. in us-east-1 and us-west-1
    # 2. in empty region intersection 
    #
    def test_get_cloudwatch_info(self):
        credentials = read_creds('default')
        service_config = {'regions': {'us-east-1': {}, 'us-west-1': {}}} #, 'cn-north-1': {}}}
        get_cloudwatch_info(credentials, service_config, ['us-east-1', 'us-west-1'], 'aws')
        get_cloudwatch_info(credentials, service_config, ['us-east-1', 'us-west-1'], 'aws-us-gov')
#        get_cloudwatch_info(credentials, service_config, ['us-gov-west-1'], 'aws-us-gov')

    #
    # Smoke tests for status display functions
    #
    def test_cloudwatch_status_init(self):
        cloudwatch_status_init()
    
    def test_cloudwatch_status(self):
        cloudwatch_status(True)
        cloudwatch_status(False)
        cloudwatch_status()

    def test_formatted_status(self):
        formatted_status(1, 42, True)
        formatted_status(42, 1, False)


