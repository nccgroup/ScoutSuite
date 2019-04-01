import json

from getpass import getpass

from azure.common.credentials import ServicePrincipalCredentials, UserPassCredentials, get_azure_cli_credentials
from azure.mgmt.resource import SubscriptionClient
from msrestazure.azure_active_directory import MSIAuthentication

from ScoutSuite.core.console import print_error, print_exception
from ScoutSuite.providers.base.authentication_strategy import AuthenticationStrategy, AuthenticationException


class AzureCredentials:

    def __init__(self, credentials, subscription_id, aws_account_id):
        self.credentials = credentials
        self.subscription_id = subscription_id
        self.aws_account_id = aws_account_id


class AzureAuthenticationStrategy(AuthenticationStrategy):

    def authenticate(self, cli=None, msi=None, service_principal=None, file_auth=None, user_account=None,
                     tenant_id=None, subscription_id=None, client_id=None, client_secret=None, username=None,
                     password=None, **kargs):
        """
        Implements authentication for the Azure provider
        """
        try:
            if cli:
                # TODO: Remove aws_account_id
                cli_credentials, aws_account_id = get_azure_cli_credentials()
                credentials = AzureCredentials(
                    cli_credentials, aws_account_id, aws_account_id)
                return credentials

            elif msi:
                msi_auth_credentials = MSIAuthentication()

                # Get the subscription ID
                subscription_client = SubscriptionClient(msi_auth_credentials)

                try:
                    # Tries to read the subscription list
                    subscription = next(
                        subscription_client.subscriptions.list())
                    aws_account_id = subscription.subscription_id

                except StopIteration:
                    # If the VM cannot read subscription list, ask Subscription ID:
                    aws_account_id = input('Subscription ID: ')

                credentials = AzureCredentials(
                    credentials, aws_account_id, aws_account_id)
                return credentials

            elif file_auth:
                data = json.loads(file_auth.read())
                subscription_id = data.get('subscriptionId')
                tenant_id = data.get('tenantId')
                client_id = data.get('clientId')
                client_secret = data.get('clientSecret')

                aws_account_id = tenant_id  # TODO this is for AWS

                credentials = ServicePrincipalCredentials(
                    client_id=client_id,
                    secret=client_secret,
                    tenant=tenant_id
                )

                return AzureCredentials(credentials, subscription_id, aws_account_id)

            elif service_principal:
                subscription_id = subscription_id if subscription_id else input(
                    "Subscription ID: ")
                tenant_id = tenant_id if tenant_id else input("Tenant ID: ")
                client_id = client_id if client_id else input("Client ID: ")
                client_secret = client_secret if client_secret else getpass(
                    "Client secret: ")

                credentials = ServicePrincipalCredentials(
                    client_id=client_id,
                    secret=client_secret,
                    tenant=tenant_id
                )

                return AzureCredentials(credentials, subscription_id, tenant_id)

            elif user_account:
                username = username if username else input("Username: ")
                password = password if password else getpass("Password: ")

                credentials = UserPassCredentials(username, password)

                if subscription_id:
                    aws_account_id = subscription_id
                else:
                    # Get the subscription ID
                    subscription_client = SubscriptionClient(credentials)
                    try:
                        # Tries to read the subscription list
                        subscription = next(
                            subscription_client.subscriptions.list())
                        aws_account_id = subscription.subscription_id
                    except StopIteration:
                        # If the user cannot read subscription list, ask Subscription ID:
                        aws_account_id = input('Subscription ID: ')

                return AzureCredentials(credentials, aws_account_id, aws_account_id)

        except Exception as e:
            print_error('Failed to authenticate to Azure')
            print_exception(e)
            return False
