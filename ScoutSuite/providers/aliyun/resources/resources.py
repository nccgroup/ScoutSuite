"""This module provides implementations for Resources and CompositeResources for OCI."""

import abc
import asyncio

from ScoutSuite.providers.base.configs.resources import CompositeResources
from ScoutSuite.providers.aliyun.facade.facade import AliyunFacade


class AliyunCompositeResources(CompositeResources, metaclass=abc.ABCMeta):

    """This class represents a collection of composite Resources (resources that include nested resources referred as
    their children). Classes extending AliyunCompositeResources have to define a '_children' attribute which consists of
    a list of tuples describing the children. The tuples are expected to respect the following format:
    (<child_class>, <child_name>). 'child_name' is used to indicate the name under which the child resources will be
    stored in the parent object.
    """

    def __init__(self, facade: AliyunFacade):
        self.facade = facade

    async def _fetch_children_of_all_resources(self, resources: dict, kwargs: dict):
        """This method iterates through a collection of resources and fetches all children of each resource, in a
        concurrent way.

        :param resources: list of (composite) resources
        :param kwargs: dict that maps resource parent keys to each kwargs (dict) used to retrieve child resources.
        """
        if len(resources) == 0:
            return

        tasks = {
            asyncio.ensure_future(
                self._fetch_children(resource_parent=resource_parent, **kwargs[resource_parent_key])
            ) for (resource_parent_key, resource_parent) in resources.items()
        }
        await asyncio.wait(tasks)

    async def _fetch_children(self, resource_parent, **kwargs):
        """This method fetches all children of a given resource (the so called 'resource_parent') by calling fetch_all
        method on each child defined in '_children' and then stores the fetched resources in `resource_parent` under
        the key associated with the child.

        :param resource_parent: The resource in which the children will be stored.
        :param kwargs: parameters that depend on the type of child resources, used to fetch them.
        """

        children = [(child_class(**kwargs), child_name) for (child_class, child_name) in self._children]
        # Fetch all children concurrently:
        await asyncio.wait(
            {asyncio.ensure_future(child.fetch_all()) for (child, _) in children}
        )
        # Update parent content:
        for child, name in children:

            if resource_parent.get(name) is None:
                resource_parent[name] = {}

            resource_parent[name].update(child)
            resource_parent[name + '_count'] = len(resource_parent[name])

