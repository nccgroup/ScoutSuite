import json
import logging
import requests
from getpass import getpass
from datetime import datetime, timedelta

from azure.common.credentials import ServicePrincipalCredentials, UserPassCredentials, get_azure_cli_credentials
from msrestazure.azure_active_directory import MSIAuthentication
from ScoutSuite.core.console import print_info, print_debug, print_exception
from msrestazure.azure_active_directory import AADTokenCredentials
import adal

from ScoutSuite.providers.base.authentication_strategy import AuthenticationStrategy, AuthenticationException


AUTHORITY_HOST_URI = 'https://login.microsoftonline.com'
AZURE_CLI_CLIENT_ID = "04b07795-8ddb-461a-bbee-02f9e1bf7b46"


class AzureCredentials:

    def __init__(self,
                 arm_credentials, aad_graph_credentials,
                 tenant_id=None, default_subscription_id=None,
                 context=None):

        self.arm_credentials = arm_credentials  # Azure Resource Manager API credentials
        self.aad_graph_credentials = aad_graph_credentials  # Azure AD Graph API credentials
        self.tenant_id = tenant_id
        self.default_subscription_id = default_subscription_id
        self.context = context

    def get_tenant_id(self):
        if self.tenant_id:
            return self.tenant_id
        elif 'tenant_id' in self.aad_graph_credentials.token:
            return self.aad_graph_credentials.token['tenant_id']
        else:
            # This is a last resort, e.g. for MSI authentication
            try:
                h = {'Authorization': 'Bearer {}'.format(self.arm_credentials.token['access_token'])}
                r = requests.get('https://management.azure.com/tenants?api-version=2020-01-01', headers=h)
                r2 = r.json()
                return r2.get('value')[0].get('tenantId')
            except Exception as e:
                print_exception('Unable to infer tenant ID: {}'.format(e))
                return None

    def get_credentials(self, resource):
        if resource == 'arm':
            self.arm_credentials = self.get_fresh_credentials(self.arm_credentials)
            return self.arm_credentials
        elif resource == 'aad_graph':
            self.aad_graph_credentials = self.get_fresh_credentials(self.aad_graph_credentials)
            return self.aad_graph_credentials
        else:
            raise AuthenticationException('Invalid credentials resource type')

    def get_fresh_credentials(self, credentials):
        """
        Check if credentials are outdated and if so refresh them.
        """
        if self.context and hasattr(credentials, 'token'):
            expiration_datetime = datetime.fromtimestamp(credentials.token['expires_on'])
            current_datetime = datetime.now()
            expiration_delta = expiration_datetime - current_datetime
            if expiration_delta < timedelta(minutes=5):
                return self.refresh_credential(credentials)
        return credentials

    def refresh_credential(self, credentials):
        """
        Refresh credentials
        """
        print_debug('Refreshing credentials')
        authority_uri = AUTHORITY_HOST_URI + '/' + self.get_tenant_id()
        existing_cache = self.context.cache
        context = adal.AuthenticationContext(authority_uri, cache=existing_cache)
        new_token = context.acquire_token(credentials.token['resource'],
                                          credentials.token['user_id'],
                                          credentials.token['_client_id'])

        new_credentials = AADTokenCredentials(new_token, credentials.token.get('_client_id'))
        return new_credentials


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
                arm_credentials, subscription_id, tenant_id = \
                    get_azure_cli_credentials(with_tenant=True)
                aad_graph_credentials, placeholder_1, placeholder_2 = \
                    get_azure_cli_credentials(with_tenant=True, resource='https://graph.windows.net')

            elif user_account:

                if not (username and password):
                    if not programmatic_execution:
                        username = username if username else input("Username: ")
                        password = password if password else getpass("Password: ")
                    else:
                        raise AuthenticationException('Username and/or password not set')

                arm_credentials = UserPassCredentials(username, password)
                aad_graph_credentials = UserPassCredentials(username, password,
                                                            resource='https://graph.windows.net')

            elif user_account_browser:

                authority_uri = AUTHORITY_HOST_URI + '/' + tenant_id
                context = adal.AuthenticationContext(authority_uri, api_version=None)

                # Resource Manager
                resource_uri = 'https://management.core.windows.net/'
                code = context.acquire_user_code(resource_uri, AZURE_CLI_CLIENT_ID)
                print_info('To authenticate to the Resource Manager API, use a web browser to '
                           'access {} and enter the {} code.'.format(code['verification_url'],
                                                                     code['user_code']))
                arm_token = context.acquire_token_with_device_code(resource_uri, code, AZURE_CLI_CLIENT_ID)
                arm_credentials = AADTokenCredentials(arm_token, AZURE_CLI_CLIENT_ID)

                # AAD Graph
                resource_uri = 'https://graph.windows.net'
                code = context.acquire_user_code(resource_uri, AZURE_CLI_CLIENT_ID)
                print_info('To authenticate to the Azure AD Graph API, use a web browser to '
                           'access {} and enter the {} code.'.format(code['verification_url'],
                                                                     code['user_code']))
                aad_graph_token = context.acquire_token_with_device_code(resource_uri, code, AZURE_CLI_CLIENT_ID)
                aad_graph_credentials = AADTokenCredentials(aad_graph_token, AZURE_CLI_CLIENT_ID)

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

                arm_credentials = ServicePrincipalCredentials(
                    client_id=client_id,
                    secret=client_secret,
                    tenant=tenant_id
                )

                aad_graph_credentials = ServicePrincipalCredentials(
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

                arm_credentials = ServicePrincipalCredentials(
                    client_id=client_id,
                    secret=client_secret,
                    tenant=tenant_id
                )

                aad_graph_credentials = ServicePrincipalCredentials(
                    client_id=client_id,
                    secret=client_secret,
                    tenant=tenant_id,
                    resource='https://graph.windows.net'
                )

            elif msi:

                arm_credentials = MSIAuthentication()
                aad_graph_credentials = MSIAuthentication(resource='https://graph.windows.net')

            else:
                raise AuthenticationException('Unknown authentication method')

            return AzureCredentials(arm_credentials,
                                    aad_graph_credentials,
                                    tenant_id, subscription_id,
                                    context)

        except Exception as e:
            if ', AdalError: Unsupported wstrust endpoint version. ' \
               'Current support version is wstrust2005 or wstrust13.' in e.args:
                raise AuthenticationException(
                    'You are likely authenticating with a Microsoft Account. '
                    'This authentication mode only support Azure Active Directory principal authentication.')

            raise AuthenticationException(e)
