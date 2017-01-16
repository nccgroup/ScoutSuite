from AWSScout2.utils_sns import *

#
# Test for Scout2 SNS functions
#
class TestScout2SNSUtilsClass:

    configPrintException(True)

    #
    # Test get_sns_region in us-east-1
    #
    def test_get_sns_region(self):
        # TODO: change to us-east-1
        credentials = read_creds('default')
        service_config = {'regions': {'us-east-1': {}}}
        get_sns_region(params = {'region': 'us-east-1', 'creds': credentials, 'sns_config': service_config})

    # 
    # Test get_sns_info (multiple thread of get_sns_region)
    # 1. in us-east-1 and us-west-1
    # 2. in empty region intersection 
    #
    def test_get_sns_info(self):
        credentials = read_creds('default')
        service_config = {'regions': {'us-east-1': {}, 'us-west-1': {}}} #, 'cn-north-1': {}}}
        get_sns_info(credentials, service_config, ['us-east-1', 'us-west-1'], 'aws')
        get_sns_info(credentials, service_config, ['us-east-1', 'us-west-1'], 'aws-us-gov')
#        get_sns_info(credentials, service_config, ['us-gov-west-1'], 'aws-us-gov')

    #
    # Smoke tests for status display functions
    #
    def test_sns_status_init(self):
        sns_status_init()
    
    def test_sns_status(self):
        sns_status(True)
        sns_status(False)
        sns_status()

    def test_formatted_status(self):
        formatted_status(1, 42, True)
        formatted_status(42, 1, False)


