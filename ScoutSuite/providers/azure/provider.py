# -*- coding: utf-8 -*-

import os

from opinel.utils.console import printError, printException

from ScoutSuite.providers.base.provider import BaseProvider
from ScoutSuite.providers.azure.configs.services import AzureServicesConfig

from azure.common.client_factory import get_azure_cli_credentials


class AzureCredentials:

    def __init__(self, credentials, subscription_id):
        self.credentials = credentials
        self.subscription_id = subscription_id


class AzureProvider(BaseProvider):
    """
    Implements provider for Azure
    """

    def __init__(self, project_id=None, organization_id=None,
                 report_dir=None, timestamp=None, services=[], skipped_services=[], thread_config=4, **kwargs):

        self.profile = 'azure-profile'  # TODO this is aws-specific

        self.metadata_path = '%s/metadata.json' % os.path.split(os.path.abspath(__file__))[0]

        self.provider_code = 'azure'
        self.provider_name = 'Microsoft Azure'

        self.services_config = AzureServicesConfig

        super(AzureProvider, self).__init__(report_dir, timestamp, services, skipped_services, thread_config)

    def authenticate(self, key_file=None, user_account=None, service_account=None, **kargs):
        """
        Implement authentication for the Azure provider using azure-cli.
        Refer to https://docs.microsoft.com/en-us/python/azure/python-sdk-azure-authenticate?view=azure-python.

        :return:
        """

        try:
            cli_credentials, self.aws_account_id = get_azure_cli_credentials()          #TODO: Remove aws_account_id
            self.credentials = AzureCredentials(cli_credentials, self.aws_account_id)
            return True
        except Exception as e:
            printError('Failed to authenticate to Azure')
            printException(e)
            return False

    def preprocessing(self, ip_ranges=[], ip_ranges_name_key=None):
        """
        TODO description
        Tweak the AWS config to match cross-service resources and clean any fetching artifacts

        :param ip_ranges:
        :param ip_ranges_name_key:
        :return: None
        """

        super(AzureProvider, self).preprocessing()
