import json
from getpass import getpass

from azure.common.credentials import ServicePrincipalCredentials, UserPassCredentials, get_azure_cli_credentials
from azure.mgmt.resource import SubscriptionClient
from msrestazure.azure_active_directory import MSIAuthentication
from ScoutSuite.core.console import print_info, print_exception

from ScoutSuite.providers.base.authentication_strategy import AuthenticationStrategy, AuthenticationException


class AzureCredentials:

    def __init__(self,
                 credentials, graphrbac_credentials,
                 subscription_id=None, tenant_id=None):
        self.credentials = credentials
        self.graphrbac_credentials = graphrbac_credentials
        self.subscription_id = subscription_id
        self.tenant_id = tenant_id if tenant_id else credentials.token.get('tenant_id')  # TODO does this work for MSI


class AzureAuthenticationStrategy(AuthenticationStrategy):

    def authenticate(self,
                     cli=None, user_account=None, service_principal=None, file_auth=None, msi=None,
                     tenant_id=None, subscription_id=None,
                     client_id=None, client_secret=None,
                     username=None, password=None,
                     programmatic_execution=False,
                     **kargs):
        """
        Implements authentication for the Azure provider
        """
        try:
            if cli:
                credentials, subscription_id, tenant_id = get_azure_cli_credentials(with_tenant=True)
                graphrbac_credentials, placeholder_1, placeholder_2 = get_azure_cli_credentials(with_tenant=True,
                                                                                                resource='https://graph.windows.net')

            elif user_account:

                if not (username and password):
                    if not programmatic_execution:
                        username = username if username else input("Username: ")
                        password = password if password else getpass("Password: ")
                    else:
                        AuthenticationException('Username and/or password not set')

                credentials = UserPassCredentials(username, password)
                graphrbac_credentials = UserPassCredentials(username, password,
                                                            resource='https://graph.windows.net')

                if not subscription_id:
                    # Get the subscription ID
                    subscription_client = SubscriptionClient(credentials)
                    try:
                        # Tries to read the subscription list
                        print_info('No subscription set, inferring ID')
                        subscription = next(subscription_client.subscriptions.list())
                        subscription_id = subscription.subscription_id
                        print_info('Running against the {} subscription'.format(subscription_id))
                    except StopIteration:
                        print_info('Unable to infer a subscription')
                        # If the user cannot read subscription list, ask Subscription ID:
                        if not programmatic_execution:
                            subscription_id = input('Subscription ID: ')
                        else:
                            AuthenticationException('Unable to infer a Subscription ID')

            elif service_principal:

                if not subscription_id:
                    if not programmatic_execution:
                        subscription_id = input('Subscription ID: ')
                    else:
                        AuthenticationException('No Subscription ID set')

                if not tenant_id:
                    if not programmatic_execution:
                        tenant_id = input("Tenant ID: ")
                    else:
                        AuthenticationException('No Tenant ID set')

                if not client_id:
                    if not programmatic_execution:
                        client_id = input("Client ID: ")
                    else:
                        AuthenticationException('No Client ID set')

                if not client_secret:
                    if not programmatic_execution:
                        client_secret = getpass("Client secret: ")
                    else:
                        AuthenticationException('No Client Secret set')

                credentials = ServicePrincipalCredentials(
                    client_id=client_id,
                    secret=client_secret,
                    tenant=tenant_id
                )

                graphrbac_credentials = ServicePrincipalCredentials(
                    client_id=client_id,
                    secret=client_secret,
                    tenant=tenant_id,
                    resource='https://graph.windows.net'
                )

            elif file_auth:

                data = json.loads(file_auth.read())
                subscription_id = data.get('subscriptionId')
                tenant_id = data.get('tenantId')
                client_id = data.get('clientId')
                client_secret = data.get('clientSecret')

                credentials = ServicePrincipalCredentials(
                    client_id=client_id,
                    secret=client_secret,
                    tenant=tenant_id
                )

                graphrbac_credentials = ServicePrincipalCredentials(
                    client_id=client_id,
                    secret=client_secret,
                    tenant=tenant_id,
                    resource='https://graph.windows.net'
                )

            elif msi:

                credentials = MSIAuthentication()
                graphrbac_credentials = MSIAuthentication(resource='https://graph.windows.net')

                if not subscription_id:
                    try:
                        # Get the subscription ID
                        subscription_client = SubscriptionClient(credentials)
                        print_info('No subscription set, inferring ID')
                        # Tries to read the subscription list
                        subscription = next(subscription_client.subscriptions.list())
                        subscription_id = subscription.subscription_id
                        print_info('Running against the {} subscription'.format(subscription_id))
                    except StopIteration:
                        # If the VM cannot read subscription list, ask Subscription ID:
                        if not programmatic_execution:
                            subscription_id = input('Subscription ID: ')
                        else:
                            AuthenticationException('Unable to infer a Subscription ID')

            return AzureCredentials(credentials, graphrbac_credentials, subscription_id, tenant_id)

        except Exception as e:
            raise AuthenticationException(e)
