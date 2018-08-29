# -*- coding: utf-8 -*-

import os

import googleapiclient

from oauth2client import tools
from oauth2client.client import GoogleCredentials
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.file import Storage
from googleapiclient import discovery

from ScoutSuite.providers.base.provider import BaseProvider
from providers.gcp.configs.services import GCPServicesConfig


class GCPProvider(BaseProvider):
    """
    Implements provider for AWS
    """

    def __init__(self, profile, report_dir=None, timestamp=None, services=[], skipped_services=[], thread_config=4):

        self.metadata_path = '%s/metadata.json' % os.path.split(os.path.abspath(__file__))[0]

        self.profile = profile
        self.gcp_project_id = None

        self.services = GCPServicesConfig(self.metadata, thread_config)

        super(GCPProvider, self).__init__(report_dir, timestamp, services, skipped_services, thread_config)

    def authenticate(self, profile, csv_credentials, mfa_serial, mfa_code):
        """
        Implement authentication for the AWS provider
        :return:
        """

        # TODO this is hardcoded
        path = os.path.expanduser('~')+'/client_secrets.json'
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = path
        self.credentials = GoogleCredentials.get_application_default()
        self.gcp_project_id = self.credentials._service_account_email.split('@')[1].split('.')[0]

        if self.credentials:
            return True
        else:
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
