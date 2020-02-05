from ScoutSuite.providers.azure.resources.subscriptions import Subscriptions

from .instances import Instances


class VirtualMachines(Subscriptions):
    _children = [
        (Instances, 'instances')
    ]
