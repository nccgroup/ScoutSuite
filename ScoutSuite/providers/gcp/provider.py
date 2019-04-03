import os

from ScoutSuite.core.console import print_exception, print_info
from ScoutSuite.providers.base.provider import BaseProvider
from ScoutSuite.providers.gcp.configs.services import GCPServicesConfig
from ScoutSuite.providers.gcp.utils import gcp_connect_service


class GCPProvider(BaseProvider):
    """
    Implements provider for GCP
    """

    def __init__(self, project_id=None, folder_id=None, organization_id=None, all_projects=None,
                 report_dir=None, timestamp=None, services=None, skipped_services=None, thread_config=4, **kwargs):
        services = [] if services is None else services
        skipped_services = [] if skipped_services is None else skipped_services

        self.metadata_path = '%s/metadata.json' % os.path.split(
            os.path.abspath(__file__))[0]

        self.provider_code = 'gcp'
        self.provider_name = 'Google Cloud Platform'
        self.environment = 'default'

        self.projects = []
        self.all_projects = all_projects
        self.project_id = project_id
        self.folder_id = folder_id
        self.organization_id = organization_id

        self.services_config = GCPServicesConfig
        self.credentials = kwargs['credentials']
        self._set_account_id()

        super(GCPProvider, self).__init__(report_dir, timestamp,
                                          services, skipped_services, thread_config)

    def get_report_name(self):
        """
        Returns the name of the report using the provider's configuration
        """
        if self.project_id:
            return 'gcp-{}'.format(self.project_id)
        elif self.organization_id:
            return 'gcp-{}'.format(self.organization_id)
        elif self.folder_id:
            return 'gcp-{}'.format(self.folder_id)
        else:
            return 'gcp'

    def _set_account_id(self):
        # All accessible projects
        if self.all_projects:
            # Service Account
            if self.credentials.is_service_account and hasattr(self.credentials, 'service_account_email'):
                self.account_id = self.credentials.service_account_email
            else:
                # TODO use username email
                self.account_id = 'GCP'
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

    async def fetch(self, regions=None, skipped_regions=None, partition_name=None):
        self._get_projects()
        self.services.set_projects(projects=self.projects)
        await super(GCPProvider, self).fetch(regions, skipped_regions, partition_name)

    def preprocessing(self, ip_ranges=None, ip_ranges_name_key=None):
        """
        TODO description
        Tweak the AWS config to match cross-resources and clean any fetching artifacts

        :param ip_ranges:
        :param ip_ranges_name_key:
        :return: None
        """
        ip_ranges = [] if ip_ranges is None else ip_ranges

        self._match_instances_and_snapshots()
        self._match_networks_and_instances()

        super(GCPProvider, self).preprocessing()

    def _get_projects(self):
        # All projects to which the user / Service Account has access to
        if self.all_projects:
            self.projects = self._gcp_facade_get_projects(
                parent_type='all', parent_id=None)

        # Project passed through the CLI
        elif self.project_id:
            self.projects = self._gcp_facade_get_projects(
                parent_type='project', parent_id=self.project_id)

        # Folder passed through the CLI
        elif self.folder_id:
            self.projects = self._gcp_facade_get_projects(
                parent_type='folder', parent_id=self.folder_id)

        # Organization passed through the CLI
        elif self.organization_id:
            self.projects = self._gcp_facade_get_projects(
                parent_type='organization', parent_id=self.organization_id)

        # Project inferred from default configuration
        elif self.credentials.default_project_id:
            self.projects = self._gcp_facade_get_projects(
                parent_type='project', parent_id=self.credentials.default_project_id)

        # Raise exception if none of the above
        else:
            print_info(
                "Could not infer the Projects to scan and no default Project ID was found.")

    # TODO: This should be moved to the GCP facade

    def _gcp_facade_get_projects(self, parent_type, parent_id):
        """
        Returns all the projects in a given organization or folder. For a project_id it only returns the project
        details.
        """

        if parent_type not in ['project', 'organization', 'folder', 'all']:
            return None

        projects = []

        # FIXME can't currently be done with API client library as it consumes v1 which doesn't support folders
        """

        resource_manager_client = resource_manager.Client(credentials=self.credentials)

        project_list = resource_manager_client.list_projects()

        for p in project_list:
            if p.parent['id'] == self.organization_id and p.status == 'ACTIVE':
                projects.append(p.project_id)
        """

        resource_manager_client_v1 = gcp_connect_service(
            service='cloudresourcemanager', credentials=self.credentials)
        resource_manager_client_v2 = gcp_connect_service(
            service='cloudresourcemanager-v2', credentials=self.credentials)

        try:
            if parent_type == 'project':
                project_response = resource_manager_client_v1.projects().list(filter='id:%s' %
                                                                                     parent_id).execute()
                if 'projects' in project_response.keys():
                    for project in project_response['projects']:
                        if project['lifecycleState'] == "ACTIVE":
                            projects.append(project)

            elif parent_type == 'all':
                project_response = resource_manager_client_v1.projects().list().execute()
                if 'projects' in project_response.keys():
                    for project in project_response['projects']:
                        if project['lifecycleState'] == "ACTIVE":
                            projects.append(project)
            else:

                # get parent children projects
                request = resource_manager_client_v1.projects().list(
                    filter='parent.id:%s' % parent_id)
                while request is not None:
                    response = request.execute()

                    if 'projects' in response.keys():
                        for project in response['projects']:
                            if project['lifecycleState'] == "ACTIVE":
                                projects.append(project)

                    request = resource_manager_client_v1.projects().list_next(previous_request=request,
                                                                              previous_response=response)

                # get parent children projects in children folders recursively
                folder_response = resource_manager_client_v2.folders().list(
                    parent='%ss/%s' % (parent_type, parent_id)).execute()
                if 'folders' in folder_response.keys():
                    for folder in folder_response['folders']:
                        projects.extend(self._get_projects(
                            "folder", folder['name'].strip(u'folders/')))

            print_info("Found {} project(s) to scan.".format(len(projects)))

        except Exception as e:
            print_exception('Unable to list accessible Projects: {}'.format(e))

        finally:
            return projects

    def _match_instances_and_snapshots(self):
        """
        Compare Compute Engine instances and snapshots to identify instance disks that do not have a snapshot.

        :return:
        """

        if 'computeengine' in self.services:
            for instance in self.services['computeengine']['instances'].values():
                for instance_disk in instance['disks'].values():
                    instance_disk['snapshots'] = []
                    for disk in self.services['computeengine']['snapshots'].values():
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

        if 'computeengine' in self.services:
            for network in self.services['computeengine']['networks'].values():
                network['instances'] = []
                for instance in self.services['computeengine']['instances'].values():
                    for network_interface in instance['network_interfaces']:
                        if network_interface['network'] == network['network_url']:
                            network['instances'].append(instance['id'])
