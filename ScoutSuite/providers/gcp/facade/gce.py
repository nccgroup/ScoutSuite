from ScoutSuite.core.console import print_exception
from ScoutSuite.providers.gcp.facade.basefacade import GCPBaseFacade
from ScoutSuite.providers.gcp.facade.utils import GCPFacadeUtils
from ScoutSuite.providers.utils import run_concurrently


class GCEFacade(GCPBaseFacade):
    def __init__(self):
        super(GCEFacade, self).__init__('compute', 'v1')

    async def get_disks(self, project_id, zone):
        try:
            gce_client = self._get_client()
            request = gce_client.disks().list(project=project_id, zone=zone)
            disks_group = gce_client.disks()
            return await GCPFacadeUtils.get_all('items', request, disks_group)
        except Exception as e:
            print_exception('Failed to retrieve disks: {}'.format(e))
            return []

    async def get_firewalls(self, project_id):
        try:
            gce_client = self._get_client()
            request = gce_client.firewalls().list(project=project_id)
            firewalls_group = gce_client.firewalls()
            return await GCPFacadeUtils.get_all('items', request, firewalls_group)
        except Exception as e:
            print_exception('Failed to retrieve firewalls: {}'.format(e))
            return []

    async def get_instances(self, project_id, zone):
        try:
            gce_client = self._get_client()
            request = gce_client.instances().list(project=project_id, zone=zone)
            instances_group = gce_client.instances()
            instances = await GCPFacadeUtils.get_all('items', request, instances_group)
            await self._add_metadata(project_id, instances)
            return instances
        except Exception as e:
            print_exception('Failed to retrieve compute instances: {}'.format(e))
            return []

    async def _add_metadata(self, project_id, instances):
        project = await self.get_project(project_id)
        common_instance_metadata = self.metadata_to_dict(project['commonInstanceMetadata'])
        for instance in instances:
            instance['metadata'] = self.metadata_to_dict(instance['metadata'])
            instance['commonInstanceMetadata'] = common_instance_metadata

    def metadata_to_dict(self, metadata):
        return dict((item['key'], item['value']) for item in metadata['items']) if 'items' in metadata else {}

    async def get_networks(self, project_id):
        try:
            gce_client = self._get_client()
            request = gce_client.networks().list(project=project_id)
            networks_group = gce_client.networks()
            return await GCPFacadeUtils.get_all('items', request, networks_group)
        except Exception as e:
            print_exception('Failed to retrieve networks: {}'.format(e))
            return []

    async def get_project(self, project_id):
        try:
            gce_client = self._get_client()
            return await run_concurrently(
                lambda: gce_client.projects().get(project=project_id).execute()
            )
        except Exception as e:
            print_exception('Failed to retrieve project: {}'.format(e))
            return None

    async def get_regions(self, project_id):
        try:
            gce_client = self._get_client()
            request = gce_client.regions().list(project=project_id)
            regions_group = gce_client.regions()
            return await GCPFacadeUtils.get_all('items', request, regions_group)
        except Exception as e:
            print_exception('Failed to retrieve regions: {}'.format(e))
            return []

    async def get_snapshots(self, project_id):
        try:
            gce_client = self._get_client()
            request = gce_client.snapshots().list(project=project_id)
            snapshots_group = gce_client.snapshots()
            return await GCPFacadeUtils.get_all('items', request, snapshots_group)
        except Exception as e:
            print_exception('Failed to retrieve snapshots: {}'.format(e))
            return []

    async def get_subnetwork(self, project_id, region, subnetwork_id):
        try:
            gce_client = self._get_client()
            return await run_concurrently(
                lambda: gce_client.subnetworks().get(project=project_id, region=region,
                                                     subnetwork=subnetwork_id).execute()
            )
        except Exception as e:
            print_exception('Failed to retrieve subnetwork: {}'.format(e))
            return None

    async def get_subnetworks(self, project_id, region):
        try:
            gce_client = self._get_client()
            request = gce_client.subnetworks().list(project=project_id, region=region)
            subnetworks_group = gce_client.subnetworks()
            return await GCPFacadeUtils.get_all('items', request, subnetworks_group)
        except Exception as e:
            print_exception('Failed to retrieve subnetworks: {}'.format(e))
            return []

    async def get_zones(self, project_id):
        try:
            gce_client = self._get_client()
            request = gce_client.zones().list(project=project_id)
            zones_group = gce_client.zones()
            return await GCPFacadeUtils.get_all('items', request, zones_group)
        except Exception as e:
            print_exception('Failed to retrieve zones: {}'.format(e))
            return []
