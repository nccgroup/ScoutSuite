from ScoutSuite.providers.azure.resources.base import AzureCompositeResources

from .instances import Instances

class VirtualMachines(AzureCompositeResources):
    _children = [
        (Instances, 'instances')
    ]
