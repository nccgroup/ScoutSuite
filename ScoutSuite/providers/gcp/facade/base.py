import json
import asyncio

from ScoutSuite.core.console import print_exception, print_info, print_warning, print_debug
from ScoutSuite.providers.gcp.facade.basefacade import GCPBaseFacade
from ScoutSuite.providers.gcp.facade.cloudresourcemanager import CloudResourceManagerFacade
from ScoutSuite.providers.gcp.facade.cloudsql import CloudSQLFacade
from ScoutSuite.providers.gcp.facade.memorystoreredis import MemoryStoreRedisFacade
from ScoutSuite.providers.gcp.facade.cloudstorage import CloudStorageFacade
from ScoutSuite.providers.gcp.facade.gce import GCEFacade
from ScoutSuite.providers.gcp.facade.dns import DNSFacade
from ScoutSuite.providers.gcp.facade.iam import IAMFacade
from ScoutSuite.providers.gcp.facade.kms import KMSFacade
from ScoutSuite.providers.gcp.facade.stackdriverlogging import StackdriverLoggingFacade
from ScoutSuite.providers.gcp.facade.stackdrivermonitoring import StackdriverMonitoringFacade
from ScoutSuite.providers.gcp.facade.gke import GKEFacade
from ScoutSuite.providers.gcp.facade.functions import FunctionsFacade
from ScoutSuite.providers.gcp.facade.bigquery import BigQueryFacade
from ScoutSuite.providers.gcp.facade.utils import GCPFacadeUtils
from ScoutSuite.utils import format_service_name


class GCPFacade(GCPBaseFacade):
    def __init__(self,
                 default_project_id=None, project_id=None, folder_id=None, organization_id=None, all_projects=None):
        super().__init__('cloudresourcemanager', 'v1')

        self.default_project_id = default_project_id
        self.all_projects = all_projects
        self.project_id = project_id
        self.folder_id = folder_id
        self.organization_id = organization_id

        self.cloudresourcemanager = CloudResourceManagerFacade()
        self.cloudsql = CloudSQLFacade()
        self.cloudstorage = CloudStorageFacade()
        self.memorystoreredis = MemoryStoreRedisFacade()
        self.gce = GCEFacade()
        self.functions = FunctionsFacade()
        self.bigquery = BigQueryFacade()
        self.iam = IAMFacade()
        self.kms = KMSFacade()
        self.dns = DNSFacade()
        self.stackdriverlogging = StackdriverLoggingFacade()
        self.stackdrivermonitoring = StackdriverMonitoringFacade()

        # lock to minimize concurrent calls to get_services()
        self.projects_services_lock = False
        self.projects_services = {}

        # Instantiate facades for proprietary services
        try:
            self.gke = GKEFacade(self.gce)
        except NameError as _:
            pass

    async def get_projects(self):
        try:
            # All projects to which the user / Service Account has access to
            if self.all_projects:
                return await self._get_projects_recursively(
                    parent_type='all', parent_id=None)
            # Project passed through the CLI
            elif self.project_id:
                return await self._get_projects_recursively(
                    parent_type='project', parent_id=self.project_id)
            # Folder passed through the CLI
            elif self.folder_id:
                return await self._get_projects_recursively(
                    parent_type='folder', parent_id=self.folder_id)
            # Organization passed through the CLI
            elif self.organization_id:
                return await self._get_projects_recursively(
                    parent_type='organization', parent_id=self.organization_id)
            # Project inferred from default configuration
            elif self.default_project_id:
                return await self._get_projects_recursively(
                    parent_type='project', parent_id=self.default_project_id)
            # Raise exception if none of the above
            else:
                print_info(
                    "Could not infer the Projects to scan and no default Project ID was found.")
                return []

        except Exception as e:
            print_exception(f'Failed to retrieve projects: {e}')
            return []

    async def _get_projects_recursively(self, parent_type, parent_id):
        """
        Returns all the projects in a given organization or folder. For a project_id it only returns the project
        details.

        # FIXME can't currently be done with API client library as it consumes v1 which doesn't support folders
        resource_manager_client = resource_manager.Client(credentials=self.credentials)
        project_list = resource_manager_client.list_projects()
        for p in project_list:
            if p.parent['id'] == self.organization_id and p.status == 'ACTIVE':
                projects.append(p.project_id)
        """

        if parent_type not in ['project', 'organization', 'folder', 'all']:
            return None

        resourcemanager_client = self._get_client()
        resourcemanager_client_v2 = self._build_arbitrary_client('cloudresourcemanager', 'v2', force_new=True)

        projects = []

        try:
            projects_group = resourcemanager_client.projects()

            if parent_type == 'project':
                request = resourcemanager_client.projects().list(filter='id:"%s"' % parent_id)
            elif parent_type == 'all':
                request = resourcemanager_client.projects().list()
            # get parent children projects
            else:
                request = resourcemanager_client.projects().list(filter='parent.id:"%s"' % parent_id)

                # get parent children projects in children folders recursively
                folder_request = resourcemanager_client_v2.folders().list(parent=f'{parent_type}s/{parent_id}')
                folder_response = await GCPFacadeUtils.get_all('folders', folder_request, projects_group)
                for folder in folder_response:
                    projects.extend(await self._get_projects_recursively("folder", folder['name'].strip('folders/')))

            project_response = await GCPFacadeUtils.get_all('projects', request, projects_group)
            if project_response:
                for project in project_response:
                    if project['lifecycleState'] == "ACTIVE":
                        projects.append(project)
            else:
                print_exception('No Projects Found, '
                                'you may have specified a non-existing Organization, Folder or Project')

        except Exception as e:
            if 'The service is currently unavailable' in e or 'Internal error encountered' in e:
                print_level = print_warning
            else:
                print_level = print_exception
            try:
                content = e.content.decode("utf-8")
                content_dict = json.loads(content)
                print_level(f'Unable to list accessible Projects: {content_dict.get("error").get("message")}')
            except Exception as e:
                print_level(f'Unable to list accessible Projects: {e}')

        finally:
            return projects

    async def get_enabled_services(self, project_id, attempt=1, has_lock=False):
        timeout = 60*attempt
        if project_id not in self.projects_services:
            # not locked, make query
            if has_lock or not self.projects_services_lock:
                self.projects_services_lock = True
                try:
                    serviceusage_client = self._build_arbitrary_client('serviceusage', 'v1', force_new=True)
                    services = serviceusage_client.services()
                    request = services.list(parent=f'projects/{project_id}', pageSize=200, filter="state:ENABLED")
                    services_response = await GCPFacadeUtils.get_all('services', request, services)
                    self.projects_services[project_id] = services_response
                    self.projects_services_lock = False
                    return self.projects_services[project_id]
                except Exception as e:
                    # hit quota, wait and retry
                    if ('API_SHARED_QUOTA_EXHAUSTED' in str(e) or 'RATE_LIMIT_EXCEEDED' in str(e)) and attempt <= 10:
                        print_warning(f"Service Usage quotas exceeded for project \"{project_id}\", retrying in {timeout}s")
                        await asyncio.sleep(timeout)
                        return await self.get_enabled_services(project_id, attempt + 1, has_lock=True)
                    # unknown error
                    else:
                        print_warning(f"Could not fetch the state of services for project \"{project_id}\": {e}")
                        self.projects_services_lock = False
                        return {}
            # locked, wait and retry
            else:
                if attempt <= 10:  # need to set a limit to ensure we don't hit recursion limits
                    if attempt != 1:
                        print_debug(f"Lock already acquired for get_services() on project \"{project_id}\", retrying in {timeout}s")
                        await asyncio.sleep(timeout)
                    # set a lower threshold for the first attempt so that execution runs faster when there aren't any issues
                    else:
                        await asyncio.sleep(10)
                    return await self.get_enabled_services(project_id, attempt + 1)
                else:
                    print_warning(f"Could not fetch the state of services for project \"{project_id}\", "
                                  f"exiting before hitting maximum recursion")
                    return {}
        else:
            return self.projects_services[project_id]

    async def is_api_enabled(self, project_id, service):
        """
        Given a project ID and service name, this method tries to determine if the service's API is enabled
        """

        # These are hardcoded endpoint correspondences as there's no easy way to do this.
        incorrect_endpoints = []
        # All projects have IAM policies regardless of whether the IAM API is enabled.
        if service == 'IAM':
            return True
        # These are hardcoded endpoint correspondences as there's no easy way to do this.
        elif service == 'KMS':
            endpoint = 'cloudkms'
        elif service == 'CloudStorage':
            endpoint = 'storage-component'
        elif service == 'CloudSQL':
            endpoint = 'sql-component'
        elif service == 'ComputeEngine':
            endpoint = 'compute'
        elif service == 'Functions':
            endpoint = 'cloudfunctions'
        elif service == 'BigQuery':
            endpoint = 'bigquery'
            incorrect_endpoints.append('annotation-bigquery-public-data.cloudpartnerservices.goog')
        elif service == 'KubernetesEngine':
            endpoint = 'container'
        elif service == 'StackdriverLogging':
            endpoint = 'logging'
        elif service == 'StackdriverMonitoring':
            endpoint = 'monitoring'
        elif service == 'MemoryStore':
            endpoint = 'redis'
        elif service == 'DNS':
            endpoint = 'dns'
        else:
            print_warning(f"Could not validate the state of the {format_service_name(service.lower())} API "
                          f"for project \"{project_id}\" (unknown endpoint), including it in the execution")
            return True

        try:
            enabled_services = await self.get_enabled_services(project_id)
            for s in enabled_services:
                if endpoint in s.get('name') and s.get('config').get('name') not in incorrect_endpoints:
                    print_debug(f'{format_service_name(service.lower())} API enabled for '
                                f'project \"{project_id}\", including')
                    return True
            print_info(f'{format_service_name(service.lower())} API not enabled for '
                       f'project \"{project_id}\", skipping')
            return False
        except Exception as e:
            print_warning(f"Could not validate the state of the {format_service_name(service.lower())} API "
                          f"for project \"{project_id}\": \"{e}\", including it in the execution")
            return True
