# -*- coding: utf-8 -*-

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
    :ivar customer_master_keys_count:            len(cmks)
    """

    targets = (
        ('customer_master_keys', '', '', {}, False)
    )

    def __init__(self, target_config):
        self.customer_master_keys = {}
        super(KMSConfig, self).__init__(target_config)

    ########################################
    ##### Overload to fetch credentials report before and after
    ########################################

    def fetch_all(self, credentials, regions=None, partition_name='aws', targets=None):
        self.fetch_cmks(credentials)

    ########################################
    ##### CMKs (Customer Managed Keys)
    ########################################
    def fetch_cmks(self, credentials):
        """
        Fetch the Customer Managed Keys
        """
        try:
            api_client = connect_service('kms', credentials, region_name='us-east-2', silent=True)
            cmks = api_client.list_keys()
            for index, key in enumerate(cmks['Keys']):
                cmks['Keys'][index]['rotation_status'] = \
                    api_client.get_key_rotation_status(KeyId=cmks['Keys'][index]['KeyId'])
            self.cmks = cmks

        except Exception as e:
            printError('Failed to download CMKs.')
            printException(e)
