from botocore.exceptions import ClientError
from opinel.utils.aws import connect_service, handle_truncated_response
from opinel.utils.console import printError, printException
from opinel.utils.globals import manage_dictionary

from ScoutSuite.providers.aws.configs.base import AWSBaseConfig
from ScoutSuite.utils import *


class KMSConfig(AWSBaseConfig):
    """
    Object that holds the KMS configuration

    :ivar customer_master_keys:                  Dictionnary of CMKs in the AWS account
    :ivar customer_master_keys_count:            len(customer_master_keys)
    """

    targets = (
        ('customer_master_keys', '', '', {}, False)
    )

    def __init__(self, target_config):
        self.customer_master_keys = {}
        super(KMSConfig, self).__init__(target_config)

    ########################################
    ##### Fetch information
    ########################################

    def fetch_all(self, credentials, regions=None, partition_name='aws', targets=None):
        regions = [] if regions is None else regions
        super(KMSConfig, self).fetch_all(credentials, regions, partition_name, targets)
        self.fetch_cmks(credentials)
        self.fetchstatuslogger.show(True)

    ########################################
    ##### CMKs (Customer Managed Keys)
    ########################################

    def fetch_cmks(self, credentials):
        """
        Fetch the Customer Managed Keys
        """
        try:
            api_client = connect_service('kms', credentials, region_name='us-east-2', silent=True)
            customer_master_keys = api_client.list_keys()
            #for index, key in enumerate(customer_master_keys['Keys']):
             #   customer_master_keys['Keys'][index]['rotation_status'] = \
              #      api_client.get_key_rotation_status(KeyId=customer_master_keys['Keys'][index]['KeyId'])
               # customer_master_keys['customer_master_keys_count'] = len(customer_master_keys)
            self.customer_master_keys = customer_master_keys

        except Exception as e:
            printError('Failed to download customer master keys.')
            printException(e)

    ########################################
    ##### Finalize KMS config
    ########################################

    def finalize(self):
        super(KMSConfig, self).finalize()