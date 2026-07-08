"""This module provides implementations for Resources for Kubernetes."""

from ScoutSuite.providers.kubernetes.facade import KubernetesFacade
from ScoutSuite.providers.base.resources.base import CompositeResources, Resources


class KubernetesResources(Resources):
    """This is the base class for Kubernetes resources."""

    def __init__(self, resources):
        self.resources = resources

    async def fetch_all(self):
        for version in self.resources:
            data = self.resources[version]
            self[version] = data
            self[f'''{version}_count'''] = len(data['resources'])

class KubernetesResourcesWithFacade(Resources):
    """This is the base class for Kubernetes resources."""

    def __init__(self, facade: KubernetesFacade):
        super().__init__(facade)
        self.facade = facade
    
    def save(self, data):
        if not data: return
        for version in data:
            self[version] = data[version]

class KubernetesCompositeResources(KubernetesResourcesWithFacade, CompositeResources):
    """This class represents a collection of KubernetesResources. Classes extending KubernetesResourcesWithFacade should define a
    "_children" attribute which consists of a list of tuples describing the children. The tuples are expected to
    respect the following format: (<child_class>, <child_name>). The child_name is used by indicates the name under
    which the child will be stored in the parent object.
    """

    async def fetch_all(self):
        for child_class, child_name in self._children:
            data: KubernetesResourcesWithFacade = child_class(self.facade)
            await data.fetch_all()

            self[child_name] = {}
            for version in data:
                self[child_name][version] = 1
                self[f'{child_name}_{version}'] = data[version]
                self[f'{child_name}_{version}_count'] = len(data[version]['resources'])