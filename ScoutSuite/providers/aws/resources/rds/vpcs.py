from ScoutSuite.providers.aws.resources.vpcs import Vpcs
from ScoutSuite.providers.aws.resources.rds.instances import RDSInstances
from ScoutSuite.providers.aws.resources.rds.snapshots import Snapshots
from ScoutSuite.providers.aws.resources.rds.subnetgroups import SubnetGroups


class RDSVpcs(Vpcs):
    _children = [
        (RDSInstances, 'instances'),
        (Snapshots, 'snapshots'),
        (SubnetGroups, 'subnet_groups'),
    ]
    
    def __init__(self, facade, scope: dict):
        super(RDSVpcs, self).__init__(facade, scope, add_ec2_classic=True)
