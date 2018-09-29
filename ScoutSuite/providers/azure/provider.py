# -*- coding: utf-8 -*-

import os

import google.auth
from opinel.utils.console import printError, printException

from ScoutSuite.providers.base.provider import BaseProvider
from ScoutSuite.providers.azure.configs.services import AzureServicesConfig

from azure.common.credentials import ServicePrincipalCredentials

class AzureCredentials():

    def __init__(self, credentials, subscription_id):
        self.credentials = credentials
        self.subscription_id = subscription_id

class AzureProvider(BaseProvider):
    """
    Implements provider for AWS
    """

    def __init__(self, project_id=None, organization_id=None,
                 report_dir=None, timestamp=None, services=[], skipped_services=[], thread_config=4, **kwargs):

        self.profile = 'aws-profile'  # TODO this is aws-specific

        self.metadata_path = '%s/metadata.json' % os.path.split(os.path.abspath(__file__))[0]

        self.provider_code = 'azure'
        self.provider_name = 'Microsoft Azure'

        self.services_config = AzureServicesConfig

        super(AzureProvider, self).__init__(report_dir, timestamp, services, skipped_services, thread_config)

    def authenticate(self, key_file=None, user_account=None, service_account=None, **kargs):
        """
        Implement authentication for the GCP provider
        Refer to https://google-auth.readthedocs.io/en/stable/reference/google.auth.html.

        :return:
        """

        try:

            # TODO this is temporary
            import os
            # Azure subscription
            SUBSCRIPTION_ID = os.environ['SUBSCRIPTION_ID']
            # Tenant ID for your Azure Subscription
            TENANT_ID = os.environ['TENANT_ID']
            # Your Service Principal App ID
            CLIENT = os.environ['CLIENT']
            # Your Service Principal Password
            KEY = os.environ['KEY']

            self.aws_account_id = TENANT_ID # TODO this is for AWS

            credentials = ServicePrincipalCredentials(
                client_id=CLIENT,
                secret=KEY,
                tenant=TENANT_ID
            )

            self.credentials = AzureCredentials(credentials, SUBSCRIPTION_ID)

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
