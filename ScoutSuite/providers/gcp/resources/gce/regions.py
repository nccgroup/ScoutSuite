from ScoutSuite.providers.gcp.resources.regions import Regions
from ScoutSuite.providers.gcp.resources.gce.subnetworks import Subnetworks
from ScoutSuite.providers.gcp.resources.gce.forwarding_rules import ForwardingRules


class GCERegions(Regions):
    _children = [
        (Subnetworks, 'subnetworks'),
        (ForwardingRules, "forwarding_rules"),
    ]
