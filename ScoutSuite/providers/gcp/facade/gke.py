import re

from ScoutSuite.core.console import print_exception
from ScoutSuite.providers.gcp.facade.base import GCPBaseFacade
from ScoutSuite.providers.utils import run_concurrently, get_and_set_concurrently


class GKEFacade(GCPBaseFacade):
    def __init__(self, gce_facade):
        super(GKEFacade, self).__init__('container', 'v1beta1')
        self._gce_facade = gce_facade

    async def get_clusters(self, project_id):
        try:
            gke_client = self._get_client()
            response = await run_concurrently(
                lambda: gke_client.projects().locations().clusters().list(parent=f"projects/{project_id}/locations/-").execute()
            )
            clusters = response.get('clusters', [])
            await get_and_set_concurrently([self._get_and_set_private_google_access_enabled],
                                           clusters, project_id=project_id)
            return clusters
        except Exception as e:
            print_exception('Failed to retrieve clusters: {}'.format(e))
            return []

    async def _get_and_set_private_google_access_enabled(self, cluster, project_id):
        try:
            region = self._get_cluster_region(cluster)
            subnetwork = await self._gce_facade.get_subnetwork(project_id, region, cluster['subnetwork'])
            if subnetwork:
                cluster['privateIpGoogleAccess'] = subnetwork.get('privateIpGoogleAccess')
            else:
                cluster['privateIpGoogleAccess'] = None
        except Exception as e:
            print_exception('Failed to retrieve cluster private IP Google access config: {}'.format(e))
            cluster['privateIpGoogleAccess'] = None

    # The cluster location is given as <region>-<zone>. See the the following link for more info: 
    # https://cloud.google.com/compute/docs/regions-zones/#identifying_a_region_or_zone
    def _get_cluster_region(self, cluster):
        region_regex = re.compile("^([\\w]+-[\\w]+)")
        result = region_regex.search(cluster['location'])
        return result.group(1)
