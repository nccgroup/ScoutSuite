import json
import logging
from getpass import getpass

from azure.common.credentials import ServicePrincipalCredentials, UserPassCredentials, get_azure_cli_credentials
from azure.mgmt.resource import SubscriptionClient
from msrestazure.azure_active_directory import MSIAuthentication
from ScoutSuite.core.console import print_info

from ScoutSuite.providers.base.authentication_strategy import AuthenticationStrategy, AuthenticationException


class AzureCredentials:

    def __init__(self, credentials, graphrbac_credentials):
        self.credentials = credentials  # Azure Resource Manager API credentials
        self.graphrbac_credentials = graphrbac_credentials  # Azure AD Graph API credentials


class AzureAuthenticationStrategy(AuthenticationStrategy):

    def authenticate(self,
                     cli=None, user_account=None, service_principal=None, file_auth=None, msi=None,
                     tenant_id=None,
                     client_id=None, client_secret=None,
                     username=None, password=None,
                     programmatic_execution=False,
                     **kargs):
        """
        Implements authentication for the Azure provider
        """
        try:

            # Set logging level to error for libraries as otherwise generates a lot of warnings
            logging.getLogger('adal-python').setLevel(logging.ERROR)
            logging.getLogger('msrest').setLevel(logging.ERROR)
            logging.getLogger('urllib3').setLevel(logging.ERROR)

            if cli:
                credentials, subscription_id, tenant_id = get_azure_cli_credentials(with_tenant=True)
                graphrbac_credentials, placeholder_1, placeholder_2 = \
                    get_azure_cli_credentials(with_tenant=True, resource='https://graph.windows.net')

            elif user_account:

                if not (username and password):
                    if not programmatic_execution:
                        username = username if username else input("Username: ")
                        password = password if password else getpass("Password: ")
                    else:
                        raise AuthenticationException('Username and/or password not set')

                credentials = UserPassCredentials(username, password)
                graphrbac_credentials = UserPassCredentials(username, password,
                                                            resource='https://graph.windows.net')


            elif service_principal:

                if not tenant_id:
                    if not programmatic_execution:
                        tenant_id = input("Tenant ID: ")
                    else:
                        raise AuthenticationException('No Tenant ID set')

                if not client_id:
                    if not programmatic_execution:
                        client_id = input("Client ID: ")
                    else:
                        raise AuthenticationException('No Client ID set')

                if not client_secret:
                    if not programmatic_execution:
                        client_secret = getpass("Client secret: ")
                    else:
                        raise AuthenticationException('No Client Secret set')

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

            return AzureCredentials(credentials, graphrbac_credentials)

        except Exception as e:
            raise AuthenticationException(e)
