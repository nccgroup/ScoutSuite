from ScoutSuite.providers.gcp.resources.zones import Zones

class GCEZones(Zones):
    _children = [
        (Instances, 'instances'),
    ]
