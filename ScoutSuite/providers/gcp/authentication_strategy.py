import logging
import os
import warnings

import google.auth.exceptions
import google.oauth2.service_account
from google import auth
from google.auth import compute_engine

from ScoutSuite.providers.base.authentication_strategy import AuthenticationStrategy, AuthenticationException


class GCPAuthenticationStrategy(AuthenticationStrategy):

    def authenticate(self, user_account=None, service_account=None, adc=False, **kwargs):
        """
        Implements authentication for the GCP provider
        Refer to https://google-auth.readthedocs.io/en/stable/reference/google.auth.html.
        """

        try:

            # Set logging level to error for libraries as otherwise generates a lot of warnings
            logging.getLogger('googleapiclient').setLevel(logging.ERROR)
            logging.getLogger('google.auth').setLevel(logging.ERROR)
            logging.getLogger('google_auth_httplib2').setLevel(logging.ERROR)
            logging.getLogger('urllib3').setLevel(logging.ERROR)

            if user_account:
                # disable GCP warning about using User Accounts
                warnings.filterwarnings("ignore", "Your application has authenticated using end user credentials")
            elif service_account:
                client_secrets_path = os.path.abspath(service_account)
                os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = client_secrets_path
            elif adc:
                # Intentionally no-op: let google.auth.default() discover credentials
                # from the environment (metadata server, gcloud ADC, etc.) without
                # setting GOOGLE_APPLICATION_CREDENTIALS.
                pass
            else:
                raise AuthenticationException('Failed to authenticate to GCP - no supported account type')

            try:
                credentials, default_project_id = auth.default()
            except google.auth.exceptions.DefaultCredentialsError as e:
                if adc:
                    raise AuthenticationException(
                        '--adc requires ScoutSuite to be running inside a GCP environment '
                        '(GCE, Cloud Run, or GKE) with an attached service account, '
                        'or gcloud ADC configured locally. '
                        f'Original error: {e}'
                    )
                raise AuthenticationException(e)

            if not credentials:
                if adc:
                    raise AuthenticationException(
                        '--adc requires ScoutSuite to be running inside a GCP environment '
                        '(GCE, Cloud Run, or GKE) with an attached service account, '
                        'or gcloud ADC configured locally. No credentials were found.'
                    )
                raise AuthenticationException('No credentials')

            is_sa = (
                service_account is not None
                or isinstance(credentials, compute_engine.Credentials)
                or isinstance(credentials, google.oauth2.service_account.Credentials)
            )
            credentials.is_service_account = is_sa
            credentials.default_project_id = default_project_id

            if adc and isinstance(credentials, compute_engine.Credentials):
                # Preserve the service_account_email attribute that the metadata server
                # populates on compute_engine.Credentials objects.
                credentials.service_account_email = credentials.service_account_email

            return credentials

        except Exception as e:
            raise AuthenticationException(e)
