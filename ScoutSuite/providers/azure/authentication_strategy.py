import json
import logging
from getpass import getpass

import requests
from ScoutSuite.core.console import print_exception

from azure.identity import UsernamePasswordCredential, AzureCliCredential, ClientSecretCredential, \
    ManagedIdentityCredential, DeviceCodeCredential
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

    def get_tenant_id(self):
        if self.tenant_id:
            return self.tenant_id
        elif hasattr(self.identity_credentials, 'tenant_id'):
            return self.identity_credentials['tenant_id']

        else:
            # Additional request for CLI & MSI authentication
            try:
                access_token = self.identity_credentials.get_token("https://management.core.windows.net/.default")
                h = {'Authorization': f'Bearer {access_token.token}'}
                r = requests.get('https://management.azure.com/tenants?api-version=2020-01-01', headers=h)
                r2 = r.json()
                return r2.get('value')[0].get('tenantId')
            except Exception as e:
                print_exception(f'Unable to infer tenant ID: {e}')
                return None

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
            logging.getLogger('azure.identity').setLevel(logging.ERROR)
            logging.getLogger('azure.core.pipeline').setLevel(logging.ERROR)

            context = None

            if cli:
                identity_credentials = AzureCliCredential()

            elif user_account:

                if not (username and password):
                    if not programmatic_execution:
                        username = username if username else input("Username: ")
                        password = password if password else getpass("Password: ")
                    else:
                        raise AuthenticationException('Username or password not set')

                identity_credentials = UsernamePasswordCredential(AZURE_CLI_CLIENT_ID, username, password,
                                                                  authority=AUTHORITY_HOST_URI, tenant_id=tenant_id)

            elif user_account_browser:

                identity_credentials = DeviceCodeCredential(authority=AUTHORITY_HOST_URI,tenant_id=tenant_id,client_id=AZURE_CLI_CLIENT_ID)

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
                identity_credentials = ManagedIdentityCredential()

            else:
                raise AuthenticationException('Unknown authentication method')

            # Getting token to authenticate and detect AuthenticationException
            identity_credentials.get_token("https://management.core.windows.net/.default")

            return AzureCredentials(
                identity_credentials,
                tenant_id, subscription_id,
                context)

        except Exception as e:
            if 'Authentication failed: Unable to find wstrust endpoint from MEX. This typically happens when ' \
               'attempting MSA accounts. More details available here. ' \
               'https://github.com/AzureAD/microsoft-authentication-library-for-python/' \
               'wiki/Username-Password-Authentication' in e.args:

                raise AuthenticationException(
                    'You are likely authenticating with a Microsoft Account. '
                    'This authentication mode only support Azure Active Directory principal authentication.')
            raise AuthenticationException(e)
