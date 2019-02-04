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
                     azure_service_principal=None, azure_file_auth=None, azure_user_credentials=None,
                     azure_tenant_id=None, azure_subscription_id=None, azure_client_id=None, azure_client_secret=None,
                     azure_username=None, azure_password=None, **kargs):
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
                data = json.loads(azure_file_auth.read())
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
                azure_subscription_id = azure_subscription_id if azure_subscription_id else input("Subscription ID: ")
                azure_tenant_id = azure_tenant_id if azure_tenant_id else input("Tenant ID: ")
                azure_client_id = azure_client_id if azure_client_id else input("Client ID: ")
                azure_client_secret = azure_client_secret if azure_client_secret else getpass("Client secret: ")

                self.aws_account_id = azure_subscription_id  # TODO this is for AWS

                credentials = ServicePrincipalCredentials(
                    client_id=azure_client_id,
                    secret=azure_client_secret,
                    tenant=azure_tenant_id
                )

                self.credentials = AzureCredentials(credentials, azure_subscription_id)

                return True
            elif azure_user_credentials:
                azure_username = azure_username if azure_username else input("Username: ")
                azure_password = azure_password if azure_password else getpass("Password: ")

                credentials = UserPassCredentials(azure_username, azure_password)

                if azure_subscription_id:
                    self.aws_account_id = azure_subscription_id
                else:
                    # Get the subscription ID
                    subscription_client = SubscriptionClient(credentials)
                    try:
                        # Tries to read the subscription list
                        subscription = next(subscription_client.subscriptions.list())
                        self.aws_account_id = subscription.subscription_id
                    except StopIteration:
                        # If the user cannot read subscription list, ask Subscription ID:
                        self.aws_account_id = input('Subscription ID: ')

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
