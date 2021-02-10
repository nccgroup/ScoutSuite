import json
import logging

import msal
import requests
from getpass import getpass
from datetime import datetime, timedelta

from azure.common.credentials import ServicePrincipalCredentials, get_azure_cli_credentials
from azure.identity import UsernamePasswordCredential, AzureCliCredential, ClientSecretCredential, \
    ManagedIdentityCredential, InteractiveBrowserCredential, ChainedTokenCredential
from msrestazure.azure_active_directory import MSIAuthentication
from ScoutSuite.core.console import print_info, print_debug, print_exception
from msrestazure.azure_active_directory import AADTokenCredentials
from ScoutSuite.providers.base.authentication_strategy import AuthenticationStrategy, AuthenticationException

AUTHORITY_HOST_URI = 'https://login.microsoftonline.com/'

AZURE_CLI_CLIENT_ID = "04b07795-8ddb-461a-bbee-02f9e1bf7b46"


class AzureCredentials:

    def __init__(self,
                 identity_credentials,
                 tenant_id=None, default_subscription_id=None,
                 context=None):

        # self.arm_credentials = arm_credentials  # Azure Resource Manager API credentials
        # self.aad_graph_credentials = aad_graph_credentials  # Azure AD Graph API credentials
        self.identity_credentials = identity_credentials  # Azure Resource Manager API credentials

        self.tenant_id = tenant_id
        self.default_subscription_id = default_subscription_id
        self.context = context

    # def get_tenant_id(self):
    #     if self.tenant_id:
    #         return self.tenant_id
    #     elif 'tenant_id' in self.identity_credentials._tenant_id:
    #         return self.identity_credentials._tenant_id
    #     else:
    #         # This is a last resort, e.g. for MSI authentication
    #         try:
    #             h = {'Authorization': 'Bearer {}'.format(self.identity_credentials._cache.CredentialType.ACCESS_TOKEN)}
    #             r = requests.get('https://management.azure.com/tenants?api-version=2020-01-01', headers=h)
    #             r2 = r.json()
    #             return r2.get('value')[0].get('tenantId')
    #         except Exception as e:
    #             print_exception('Unable to infer tenant ID: {}'.format(e))
    #             return None
    #
    # def get_credentials(self, resource):
    #     self.identity_credentials = self.get_fresh_credentials(self.identity_credentials)
    #     return self.identity_credentials
    #
    # def get_fresh_credentials(self, credentials):
    #     """
    #     Check if credentials are outdated and if so refresh them.
    #     """
    #
    #     if self.context and hasattr(credentials, 'token'):
    #         expiration_datetime = datetime.fromtimestamp(credentials.token['expires_on'])
    #         current_datetime = datetime.now()
    #         expiration_delta = expiration_datetime - current_datetime
    #         if expiration_delta < timedelta(minutes=50000):
    #             return self.refresh_credential(credentials)
    #     return credentials
    #
    # def refresh_credential(self, credentials):
    #     """
    #     Refresh credentials
    #     """
    #     print_debug('Refreshing credentials')
    #     authority_uri = AUTHORITY_HOST_URI + self.get_tenant_id()
    #     existing_cache = self.context.cache
    #
    #     client = msal.PublicClientApplication(AZURE_CLI_CLIENT_ID, token_cache=existing_cache,
    #                                           authority=authority_uri)
    #
    #     scopes = [credentials.resource + "/.default"]
    #
    #     new_token = client.acquire_token_by_refresh_token(credentials.token['refresh_token'], scopes)
    #
    #     new_credentials = AADTokenCredentials(new_token, credentials.token.get('_client_id'))
    #     return new_credentials


class AzureAuthenticationStrategy(AuthenticationStrategy):

    def authenticate(self,
                     cli=None, user_account=None, user_account_browser=None,
                     service_principal=None, file_auth=None, msi=None,
                     tenant_id=None,
                     subscription_id=None,
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
            logging.getLogger('msrestazure.azure_active_directory').setLevel(logging.ERROR)
            logging.getLogger('urllib3').setLevel(logging.ERROR)
            logging.getLogger('cli.azure.cli.core').setLevel(logging.ERROR)

            context = None

            if cli:
                identity_credentials = AzureCliCredential()
                # arm_credentials, subscription_id, tenant_id = \
                #     get_azure_cli_credentials(with_tenant=True)
                # aad_graph_credentials, placeholder_1, placeholder_2 = \
                #     get_azure_cli_credentials(with_tenant=True, resource='https://graph.microsoft.com')

            elif user_account:

                if not (username and password and tenant_id):
                    if not programmatic_execution:
                        tenant_id = tenant_id if tenant_id else input("Tenant ID: ")
                        username = username if username else input("Username: ")
                        password = password if password else getpass("Password: ")
                    else:
                        raise AuthenticationException('Username, Tenant ID and/or password not set')

                # client = msal.PublicClientApplication(AZURE_CLI_CLIENT_ID, authority=AUTHORITY_HOST_URI + tenant_id)

                # Resource Manager
                # resource_uri = 'https://management.core.windows.net/'
                # scopes = [resource_uri + "/.default"]
                # arm_token = client.acquire_token_by_username_password(username, password, scopes)
                # arm_credentials = AADTokenCredentials(arm_token, AZURE_CLI_CLIENT_ID)
                #
                # # AAD Graph
                # resource_uri = 'https://graph.microsoft.com'
                # scopes = [resource_uri + "/.default"]
                # aad_graph_token = client.acquire_token_by_username_password(username, password, scopes)
                # aad_graph_credentials = AADTokenCredentials(aad_graph_token, AZURE_CLI_CLIENT_ID)

                identity_credentials = UsernamePasswordCredential(AZURE_CLI_CLIENT_ID, username, password,
                                                                  authority=AUTHORITY_HOST_URI)

            elif user_account_browser:

                # client = msal.PublicClientApplication(AZURE_CLI_CLIENT_ID)

                # Resource Manager
                # resource_uri = 'https://management.core.windows.net/'
                # scopes = [resource_uri + "/.default"]
                # code = client.initiate_device_flow(scopes)
                # print_info('To authenticate to the Resource Manager API, use a web browser to '
                #            'access {} and enter the {} code.'.format(code['verification_uri'],
                #                                                      code['user_code']))
                # arm_token = client.acquire_token_by_device_flow(code)
                # arm_credentials = AADTokenCredentials(arm_token, AZURE_CLI_CLIENT_ID)

                # # AAD Graph
                # resource_uri = 'https://graph.microsoft.com'
                # scopes = [resource_uri + "/.default"]
                # code = client.initiate_device_flow(scopes)
                # print_info('To authenticate to the microsoft Graph API, use a web browser to '
                #            'access {} and enter the {} code.'.format(code['verification_uri'],
                #                                                      code['user_code']))
                # aad_graph_token = client.acquire_token_by_device_flow(code)
                # aad_graph_credentials = AADTokenCredentials(aad_graph_token, AZURE_CLI_CLIENT_ID)

                identity_credentials = InteractiveBrowserCredential()

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

                identity_credentials = ClientSecretCredential(
                    client_id=client_id,
                    client_secret=client_secret,
                    tenant_id=tenant_id
                )
                # arm_credentials = ServicePrincipalCredentials(
                #     client_id=client_id,
                #     secret=client_secret,
                #     tenant=tenant_id
                # )
                #
                # aad_graph_credentials = ServicePrincipalCredentials(
                #     client_id=client_id,
                #     secret=client_secret,
                #     tenant=tenant_id,
                #     resource='https://graph.microsoft.com'
                # )

            elif file_auth:

                data = json.loads(file_auth.read())
                tenant_id = data.get('tenantId')
                client_id = data.get('clientId')
                client_secret = data.get('clientSecret')

                identity_credentials = ClientSecretCredential(
                    client_id=client_id,
                    client_secret=client_secret,
                    tenant_id=tenant_id
                )
                # arm_credentials = ServicePrincipalCredentials(
                #     client_id=client_id,
                #     secret=client_secret,
                #     tenant=tenant_id
                # )
                #
                # aad_graph_credentials = ServicePrincipalCredentials(
                #     client_id=client_id,
                #     secret=client_secret,
                #     tenant=tenant_id,
                #     resource='https://graph.microsoft.com'
                # )

            elif msi:
                identity_credentials = ManagedIdentityCredential()
                # arm_credentials = MSIAuthentication()
                # aad_graph_credentials = MSIAuthentication(resource='https://graph.microsoft.com')

            else:
                raise AuthenticationException('Unknown authentication method')

            return AzureCredentials(
                identity_credentials,
                tenant_id, subscription_id,
                context)

        except Exception as e:
            if ', AdalError: Unsupported wstrust endpoint version. ' \
               'Current support version is wstrust2005 or wstrust13.' in e.args:
                raise AuthenticationException(
                    'You are likely authenticating with a Microsoft Account. '
                    'This authentication mode only support Azure Active Directory principal authentication.')

            raise AuthenticationException(e)
