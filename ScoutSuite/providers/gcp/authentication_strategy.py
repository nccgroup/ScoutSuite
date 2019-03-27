import google
import os
import warnings

from ScoutSuite.core.console import print_error
from ScoutSuite.providers.base.authentication_strategy import AuthenticationStrategy, AuthenticationException


class GCPAuthenticationStrategy(AuthenticationStrategy):

    def authenticate(self, user_account=None, service_account=None, **kargs):
        """
        Implements authentication for the GCP provider
        Refer to https://google-auth.readthedocs.io/en/stable/reference/google.auth.html.
        """

        if user_account:
            # disable GCP warning about using User Accounts
            warnings.filterwarnings(
                "ignore", "Your application has authenticated using end user credentials")
            pass  # Nothing more to do
        elif service_account:
            client_secrets_path = os.path.abspath(service_account)
            os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = client_secrets_path
        else:
            print_error(
                'Failed to authenticate to GCP - no supported account type')
            raise AuthenticationException()

        credentials, default_project_id = google.auth.default()
        if not credentials:
            raise AuthenticationException()

        credentials.is_service_account = service_account is not None
        credentials.default_project_id = default_project_id
        return credentials
