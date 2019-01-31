# -*- coding: utf-8 -*-

import os
import json

from getpass import getpass

from opinel.utils.console import printError, printException

from ScoutSuite.providers.base.provider import BaseProvider
from ScoutSuite.providers.azure.configs.services import AzureServicesConfig

from msrestazure.azure_active_directory import MSIAuthentication
from azure.mgmt.resource import SubscriptionClient
from azure.common.credentials import ServicePrincipalCredentials, UserPassCredentials, get_azure_cli_credentials


class AzureCredentials:

    def __init__(self, credentials, subscription_id):
        self.credentials = credentials
        self.subscription_id = subscription_id


class AzureProvider(BaseProvider):
    """
    Implements provider for Azure
    """

    def __init__(self, project_id=None, organization_id=None,
                 report_dir=None, timestamp=None, services=None, skipped_services=None, thread_config=4, **kwargs):
        services = [] if services is None else services
        skipped_services = [] if skipped_services is None else skipped_services

        self.profile = 'azure-profile'  # TODO this is aws-specific

        self.metadata_path = '%s/metadata.json' % os.path.split(os.path.abspath(__file__))[0]

        self.provider_code = 'azure'
        self.provider_name = 'Microsoft Azure'

        self.services_config = AzureServicesConfig

        super(AzureProvider, self).__init__(report_dir, timestamp, services, skipped_services, thread_config)

    def authenticate(self, key_file=None, user_account=None, service_account=None, azure_cli=None, azure_msi=None,
                     azure_service_principal=None, azure_file_auth=None, azure_user_credentials=None, **kargs):
        """
        Implements authentication for the Azure provider using azure-cli.
        Refer to https://docs.microsoft.com/en-us/python/azure/python-sdk-azure-authenticate?view=azure-python.

        :return:
        """

        try:
            if azure_cli:
                cli_credentials, self.aws_account_id = get_azure_cli_credentials()  # TODO: Remove aws_account_id
                self.credentials = AzureCredentials(cli_credentials, self.aws_account_id)
                return True
            elif azure_msi:
                credentials = MSIAuthentication()

                # Get the subscription ID
                subscription_client = SubscriptionClient(credentials)
                try:
                    # Tries to read the subscription list
                    subscription = next(subscription_client.subscriptions.list())
                    self.aws_account_id = subscription.subscription_id
                except StopIteration:
                    # If the VM cannot read subscription list, ask Subscription ID:
                    self.aws_account_id = input('Subscription ID: ')

                self.credentials = AzureCredentials(credentials, self.aws_account_id)
                return True
            elif azure_file_auth:
                with open(azure_file_auth) as f:
                    data = json.loads(f.read())
                    subscription_id = data.get('subscriptionId')
                    tenant_id = data.get('tenantId')
                    client_id = data.get('clientId')
                    client_secret = data.get('clientSecret')

                    self.aws_account_id = tenant_id  # TODO this is for AWS

                    credentials = ServicePrincipalCredentials(
                        client_id=client_id,
                        secret=client_secret,
                        tenant=tenant_id
                    )

                    self.credentials = AzureCredentials(credentials, subscription_id)

                    return True
            elif azure_service_principal:
                subscription_id = input("Subscription ID: ")
                tenant_id = input("Tenant ID: ")
                client_id = input("Client ID: ")
                client_secret = getpass("Client secret: ")

                self.aws_account_id = tenant_id  # TODO this is for AWS

                credentials = ServicePrincipalCredentials(
                    client_id=client_id,
                    secret=client_secret,
                    tenant=tenant_id
                )

                self.credentials = AzureCredentials(credentials, subscription_id)

                return True
            elif azure_user_credentials:
                username = input("Username: ")
                password = getpass("Password: ")

                credentials = UserPassCredentials(username, password)
                self.aws_account_id = ""  # TODO this is for AWS
                self.credentials = AzureCredentials(credentials, self.aws_account_id)
                return True
        except Exception as e:
            printError('Failed to authenticate to Azure')
            printException(e)
            return False

    def preprocessing(self, ip_ranges=None, ip_ranges_name_key=None):
        """
        TODO description
        Tweak the AWS config to match cross-service resources and clean any fetching artifacts

        :param ip_ranges:
        :param ip_ranges_name_key:
        :return: None
        """
        ip_ranges = [] if ip_ranges is None else ip_ranges
        super(AzureProvider, self).preprocessing()
