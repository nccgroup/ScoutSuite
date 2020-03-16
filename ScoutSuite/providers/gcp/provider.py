import os

from ScoutSuite.providers.base.provider import BaseProvider
from ScoutSuite.providers.gcp.services import GCPServicesConfig


class GCPProvider(BaseProvider):
    """
    Implements provider for GCP
    """

    def __init__(self,
                 project_id=None, folder_id=None, organization_id=None, all_projects=None,
                 report_dir=None, timestamp=None, services=None, skipped_services=None, result_format='json', **kwargs):
        services = [] if services is None else services
        skipped_services = [] if skipped_services is None else skipped_services

        self.metadata_path = '%s/metadata.json' % os.path.split(
            os.path.abspath(__file__))[0]

        self.provider_code = 'gcp'
        self.provider_name = 'Google Cloud Platform'
        self.environment = 'default'

        self.all_projects = all_projects
        self.project_id = project_id
        self.folder_id = folder_id
        self.organization_id = organization_id

        self.credentials = kwargs['credentials']
        self._set_account_id()

        self.services = GCPServicesConfig(self.credentials, self.credentials.default_project_id,
                                          self.project_id, self.folder_id, self.organization_id, self.all_projects)

        self.result_format = result_format

        super(GCPProvider, self).__init__(report_dir, timestamp,
                                          services, skipped_services, result_format)

    def get_report_name(self):
        """
        Returns the name of the report using the provider's configuration
        """
        if self.account_id:
            return 'gcp-{}'.format(self.account_id)
        else:
            printError('Failed to authenticate to GCP - no supported account type')
            return False

        try:

            self.credentials, project_id = google.auth.default()
            if self.credentials:

                # Project passed through the CLI
                if self.project_id:
                    self.projects = self._get_projects(parent_type='project',
                                                       parent_id=self.project_id)
                    self.aws_account_id = self.project_id  # FIXME this is for AWS
                    self.profile = self.project_id  # FIXME this is for AWS

                # Folder passed through the CLI
                elif self.folder_id:
                    self.projects = self._get_projects(parent_type='folder',
                                                       parent_id=self.folder_id)
                    self.aws_account_id = self.folder_id  # FIXME this is for AWS
                    self.profile = self.folder_id  # FIXME this is for AWS

                # Organization passed through the CLI
                elif self.organization_id:
                    self.projects = self._get_projects(parent_type='organization',
                                                       parent_id=self.organization_id)
                    self.aws_account_id = self.organization_id  # FIXME this is for AWS
                    self.profile = self.organization_id  # FIXME this is for AWS

                # Project inferred from default configuration and not a service account
                if project_id and not service_account:
                    self.projects = self._get_projects(parent_type='project',
                                                       parent_id=project_id)
                    self.aws_account_id = project_id  # FIXME this is for AWS
                    self.profile = project_id  # FIXME this is for AWS

                # All projects to which the user / Service Account has access to
                else:
                    # self.project_id = project_id
                    self.projects = self._get_projects(parent_type='all',
                                                       parent_id=None)
                    if service_account and hasattr(self.credentials, 'service_account_email'):
                        self.aws_account_id = self.credentials.service_account_email  # FIXME this is for AWS
                    else:
                        self.aws_account_id = 'GCP'  # FIXME this is for AWS

                    self.profile = 'GCP'  # FIXME this is for AWS

                # TODO this shouldn't be done here? but it has to in order to init with projects...
                self.services.set_projects(projects=self.projects)

                return True
            return 'gcp'

    def _set_account_id(self):
        # All accessible projects
        if self.all_projects:
            # Service Account
            if self.credentials.is_service_account and hasattr(self.credentials, 'service_account_email'):
                self.account_id = self.credentials.service_account_email
            else:
                # TODO use username email (can't find it...)
                self.account_id = 'user-account'
        # Project passed through the CLI
        elif self.project_id:
            self.account_id = self.project_id
        # Folder passed through the CLI
        elif self.folder_id:
            self.account_id = self.folder_id
        # Organization passed through the CLI
        elif self.organization_id:
            self.account_id = self.organization_id
        # Project inferred from default configuration
        elif self.credentials.default_project_id:
            self.account_id = self.credentials.default_project_id
        else:
            self.account_id = 'unknown-project-id'

    def preprocessing(self, ip_ranges=None, ip_ranges_name_key=None):
        """
        Tweak the GCP config to match cross-resources and clean any fetching artifacts

        :param ip_ranges:
        :param ip_ranges_name_key:
        :return: None
        """
        self._match_instances_and_snapshots()
        self._match_networks_and_instances()

        super(GCPProvider, self).preprocessing()

    def _match_instances_and_snapshots(self):
        """
        Compare Compute Engine instances and snapshots to identify instance disks that do not have a snapshot.

        :return:
        """

        if 'computeengine' in self.service_list:
            for project in self.services['computeengine']['projects'].values():
                for zone in project['zones'].values():
                    for instance in zone['instances'].values():
                        for instance_disk in instance['disks'].values():
                            instance_disk['snapshots'] = []
                            for disk in project['snapshots'].values():
                                if disk['status'] == 'READY' and disk['source_disk_url'] == instance_disk['source_url']:
                                    instance_disk['snapshots'].append(disk)

                            instance_disk['latest_snapshot'] = max(instance_disk['snapshots'],
                                                                   key=lambda x: x['creation_timestamp']) \
                                if instance_disk['snapshots'] else None

    def _match_networks_and_instances(self):
        """
        For each network, math instances in that network

        :return:
        """

        if 'computeengine' in self.service_list:
            for project in self.services['computeengine']['projects'].values():
                for network in project['networks'].values():
                    network['instances'] = []
                    for zone in project['zones'].values():
                        # Skip the counts contained in the zones dictionary
                        if zone is int:
                            continue
                        for instance in zone['instances'].values():
                            for network_interface in instance['network_interfaces']:
                                if network_interface['network'] == network['network_url']:
                                    network['instances'].append(instance['id'])
