# -*- coding: utf-8 -*-

import os

import google.auth
from opinel.utils.console import printError, printException

from ScoutSuite.providers.base.provider import BaseProvider
from ScoutSuite.providers.gcp.configs.services import GCPServicesConfig

import googleapiclient
from oauth2client.client import GoogleCredentials
from googleapiclient import discovery
from google.cloud import resource_manager


class GCPCredentials():

    def __init__(self, api_client_credentials, cloud_client_credentials):
        self.api_client_credentials = api_client_credentials
        self.cloud_client_credentials = cloud_client_credentials

class GCPProvider(BaseProvider):
    """
    Implements provider for AWS
    """

    def __init__(self, project_id=None, organization_id=None,
                 report_dir=None, timestamp=None, services=[], skipped_services=[], thread_config=4, **kwargs):

        self.profile = 'gcp-profile'  # TODO this is aws-specific

        self.metadata_path = '%s/metadata.json' % os.path.split(os.path.abspath(__file__))[0]

        self.project_id=project_id
        self.projects=[project_id]
        self.organization_id=organization_id

        self.services_config = GCPServicesConfig

        super(GCPProvider, self).__init__(report_dir, timestamp, services, skipped_services, thread_config)

    def authenticate(self, key_file=None, user_account=None, service_account=None, **kargs):
        """
        Implement authentication for the GCP provider
        Refer to https://google-auth.readthedocs.io/en/stable/reference/google.auth.html.

        :return:
        """

        if user_account:
            # disable GCP warning about using User Accounts
            import warnings
            warnings.filterwarnings("ignore", "Your application has authenticated using end user credentials")
            pass  # Nothing more to do
        elif service_account:
            client_secrets_path = os.path.abspath(key_file)  # TODO this is probably wrong
            os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = client_secrets_path
        else:
            printError('Failed to authenticate to GCP - no supported account type')
            return False

        try:

            # TODO there is probably a better way to do this
            # api_client_credentials = GoogleCredentials.get_application_default()
            # cloud_client_credentials, self.gcp_project_id = google.auth.default()
            # self.credentials = GCPCredentials(api_client_credentials, cloud_client_credentials)

            # TODO not sure why this works - there are no credentials for API client libraries
            self.credentials, project_id = google.auth.default()

            if self.credentials:
                if self.organization_id:
                    self.projects = self._get_all_projects_in_organization()
                elif not self.project_id:
                    self.projects = [project_id]

                self.aws_account_id = self.projects[0] # TODO this is for AWS

                # TODO this shouldn't be done here? but it has to in order to init with projects...
                self.services.set_projects(projects=self.projects)

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

    def _get_all_projects_in_organization(self):

        projects = []

        resource_manager_client = resource_manager.Client(credentials=self.credentials)
        b = dir(resource_manager_client)

        project_list = resource_manager_client.list_projects()

        for p in project_list:
            # project = resource_manager_client.fetch_project(p.project_id)
            if p.parent['id'] == self.organization_id and p.status == 'ACTIVE':
                projects.append(p.project_id)

        return projects
