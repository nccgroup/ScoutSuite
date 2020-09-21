from ScoutSuite.providers.gcp.resources.gke.clusters import Clusters
from ScoutSuite.providers.gcp.resources.zones import Zones


class GKEZones(Zones):
    _children = [
        (Clusters, 'clusters'),
    ]
