# -*- coding: utf-8 -*-

import os

import google.auth
from opinel.utils.console import printError, printException

from ScoutSuite.providers.base.provider import BaseProvider
from ScoutSuite.providers.gcp.configs.services import GCPServicesConfig

import googleapiclient
from oauth2client.client import GoogleCredentials
from googleapiclient import discovery


class GCPCredentials():

    def __init__(self, api_client_credentials, cloud_client_credentials):
        self.api_client_credentials = api_client_credentials
        self.cloud_client_credentials = cloud_client_credentials

class GCPProvider(BaseProvider):
    """
    Implements provider for AWS
    """

    def __init__(self, profile, report_dir=None, timestamp=None, services=[], skipped_services=[], thread_config=4):

        self.metadata_path = '%s/metadata.json' % os.path.split(os.path.abspath(__file__))[0]

        self.profile = profile
        self.gcp_project_id = None
        self.services_config = GCPServicesConfig

        super(GCPProvider, self).__init__(report_dir, timestamp, services, skipped_services, thread_config)

    def authenticate(self, client_secrets=None, **kargs):
        """
        Implement authentication for the GCP provider
        Refer to https://google-auth.readthedocs.io/en/stable/reference/google.auth.html.

        :return:
        """

        if client_secrets:
            client_secrets_path = os.path.abspath(client_secrets)  # TODO this is probably wrong
            os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = client_secrets_path
        # Currently not supported
        else:
            printError('Failed to authenticate to GCP - currently only supports service accounts')
            return False

        try:

            # TODO there is probably a better way to do this
            # api_client_credentials = GoogleCredentials.get_application_default()
            # cloud_client_credentials, self.gcp_project_id = google.auth.default()
            #
            # self.credentials = GCPCredentials(api_client_credentials, cloud_client_credentials)

            # TODO not sure why this works - there are no credentials for API client libraries
            self.credentials, self.gcp_project_id = google.auth.default()

            self.aws_account_id = self.gcp_project_id  # TODO this is for AWS

            if self.credentials:
                return True
            else:
                return False

        except google.auth.exceptions.DefaultCredentialsError as e:
            printError('Failed to authenticate to GCP')
            printException(e)
            return False

    def preprocessing(self, ip_ranges=[], ip_ranges_name_key=None):
        """
        TODO description
        Tweak the AWS config to match cross-service resources and clean any fetching artifacts

        :param ip_ranges:
        :param ip_ranges_name_key:
        :return: None
        """

        super(GCPProvider, self).preprocessing()
