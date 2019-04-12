from ScoutSuite.providers.gcp.resources.regions import Regions

class GCERegions(Regions):
    _children = [
        (Subnetworks, 'subnetworks')
    ]
