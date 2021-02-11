import json
import logging
from getpass import getpass

from azure.identity import UsernamePasswordCredential, AzureCliCredential, ClientSecretCredential, \
    ManagedIdentityCredential, InteractiveBrowserCredential
from ScoutSuite.providers.base.authentication_strategy import AuthenticationStrategy, AuthenticationException

AUTHORITY_HOST_URI = 'https://login.microsoftonline.com/'
AZURE_CLI_CLIENT_ID = "04b07795-8ddb-461a-bbee-02f9e1bf7b46"


class AzureCredentials:

    def __init__(self,
                 identity_credentials,
                 tenant_id=None, default_subscription_id=None,
                 context=None):

        self.identity_credentials = identity_credentials  # Azure Resource Manager API credentials
        self.tenant_id = tenant_id
        self.default_subscription_id = default_subscription_id
        self.context = context

    # def get_tenant_id(self):
    #     if self.tenant_id:
    #         return self.tenant_id
    #     elif 'tenant_id' in self.identity_credentials['tenant_id']:
    #         return self.identity_credentials['tenant_id']
        # else:
        #     # This is a last resort, e.g. for MSI authentication
        #     try:
        #         h = {'Authorization': 'Bearer {}'.format(self.identity_credentials._cache.CredentialType.ACCESS_TOKEN)}
        #         r = requests.get('https://management.azure.com/tenants?api-version=2020-01-01', headers=h)
        #         r2 = r.json()
        #         return r2.get('value')[0].get('tenantId')
        #     except Exception as e:
        #         print_exception('Unable to infer tenant ID: {}'.format(e))
        #         return None

    def get_credentials(self):
        return self.identity_credentials


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

            elif user_account:

                if not (username and password and tenant_id):
                    if not programmatic_execution:
                        tenant_id = tenant_id if tenant_id else input("Tenant ID: ")
                        username = username if username else input("Username: ")
                        password = password if password else getpass("Password: ")
                    else:
                        raise AuthenticationException('Username, Tenant ID and/or password not set')

                identity_credentials = UsernamePasswordCredential(AZURE_CLI_CLIENT_ID, username, password,
                                                                  authority=AUTHORITY_HOST_URI, tenant_id=tenant_id)

            elif user_account_browser:

                identity_credentials = InteractiveBrowserCredential(tenant_id=tenant_id)

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


            elif msi:
                identity_credentials = ManagedIdentityCredential(client_id=AZURE_CLI_CLIENT_ID)

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
