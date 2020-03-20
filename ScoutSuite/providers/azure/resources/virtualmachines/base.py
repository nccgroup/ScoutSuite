from ScoutSuite.providers.azure.resources.subscriptions import Subscriptions

from .instances import Instances
from .disks import Disks
from .snapshots import Snapshots
from .images import Images


class VirtualMachines(Subscriptions):
    _children = [
        (Instances, 'instances'),
        (Disks, 'disks'),
        (Snapshots, 'snapshots'),
        (Images, 'images'),
    ]
