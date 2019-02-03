from botocore.exceptions import ClientError
from opinel.utils.aws import connect_service, handle_truncated_response
from opinel.utils.console import printError, printException
from opinel.utils.globals import manage_dictionary

from ScoutSuite.providers.aws.configs.regions import RegionalServiceConfig, RegionConfig, api_clients
from ScoutSuite.utils import *


class KMSRegionConfig(RegionConfig):
    """
    KMS Configuration for a single AWS region
    """

    def parse_key(self, global_params, region, key):
        """
        Parse a single Key Management Service

        :param global_params:           Parameters shared for all regions
        :param region:                  Name of the AWS region
        :param key:                     Key
        """
        
        key_config = {}
        
        try:
            api_client = connect_service('kms', self.credentials, region_name=region, silent=True)
            customer_master_keys = api_client.list_keys()
            for index, key in enumerate(customer_master_keys['Keys']):
                customer_master_keys['Keys'][index]['rotation_status'] = \
                    api_client.get_key_rotation_status(KeyId=customer_master_keys['Keys'][index]['KeyId'])
                customer_master_keys['customer_master_keys_count'] = len(customer_master_keys)
            self.customer_master_keys = customer_master_keys

        except Exception as e:
            printError('Failed to download customer master keys.')
            printException(e)

        
########################################
# KMSConfig
########################################

class KMSConfig(RegionalServiceConfig):
    """
    KMS configuration for all AWS regions
    """

    region_config_class = KMSRegionConfig

    def __init__(self, service_metadata, thread_config=4):
        super(KMSConfig, self).__init__(service_metadata, thread_config)
