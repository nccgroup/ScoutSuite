from ScoutSuite.providers.gcp.resources.private_gke.clusters import Clusters
from ScoutSuite.providers.gcp.resources.zones import Zones


class GKEZones(Zones):
    _children = [
        (Clusters, 'clusters'),
    ]
