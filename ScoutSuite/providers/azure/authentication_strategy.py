import json
import logging
from getpass import getpass

from azure.common.credentials import ServicePrincipalCredentials, UserPassCredentials, get_azure_cli_credentials
from msrestazure.azure_active_directory import MSIAuthentication
from ScoutSuite.core.console import print_info
from msrestazure.azure_active_directory import AADTokenCredentials
import adal

from ScoutSuite.providers.base.authentication_strategy import AuthenticationStrategy, AuthenticationException


class AzureCredentials:

    def __init__(self,
                 arm_credentials, aad_graph_credentials,
                 tenant_id=None, default_subscription_id=None):

        self.arm_credentials = arm_credentials  # Azure Resource Manager API credentials
        self.aad_graph_credentials = aad_graph_credentials  # Azure AD Graph API credentials
        self.tenant_id = tenant_id
        self.default_subscription_id = default_subscription_id

    def get_tenant_id(self):
        if self.tenant_id:
            return self.tenant_id
        else:
            return self.aad_graph_credentials.token['tenant_id']


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
            logging.getLogger('urllib3').setLevel(logging.ERROR)

            if cli:
                arm_credentials, subscription_id, tenant_id = get_azure_cli_credentials(with_tenant=True)
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

                # As per https://docs.microsoft.com/en-us/samples/azure-samples/data-lake-analytics-python-auth-options
                # /authenticating-your-python-application-against-azure-active-directory/
                # The client id used above is a well known that already exists for all azure services. While it makes
                # the sample code easy to use, for production code you should use generate your own client ids for
                # your application.
                client_id = '04b07795-8ddb-461a-bbee-02f9e1bf7b46'
                authority_host_uri = 'https://login.microsoftonline.com'
                authority_uri = authority_host_uri + '/' + tenant_id
                context = adal.AuthenticationContext(authority_uri, api_version=None)

                # Resource Manager
                resource_uri = 'https://management.core.windows.net/'
                code = context.acquire_user_code(resource_uri, client_id)
                print_info('To authenticate to the Resource Manager API, use a web browser to '
                           'access {} and enter the {} code.'.format(code['verification_url'],
                                                                     code['user_code']))
                mgmt_token = context.acquire_token_with_device_code(resource_uri, code, client_id)
                arm_credentials = AADTokenCredentials(mgmt_token, client_id)
                # Graph
                resource_uri = 'https://graph.windows.net'
                code = context.acquire_user_code(resource_uri, client_id)
                print_info('To authenticate to the Azure Graph API, use a web browser to '
                           'access {} and enter the {} code.'.format(code['verification_url'],
                                                                     code['user_code']))
                mgmt_token = context.acquire_token_with_device_code(resource_uri, code, client_id)
                aad_graph_credentials = AADTokenCredentials(mgmt_token, client_id)

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

            return AzureCredentials(arm_credentials, aad_graph_credentials,
                                    tenant_id, subscription_id)

        except Exception as e:
            raise AuthenticationException(e)
