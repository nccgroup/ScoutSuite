"""This module provides implementations for Resources and CompositeResources for AWS."""

import abc
import asyncio

from ScoutSuite.providers.base.configs.resources import Resources, CompositeResources


class AWSResources(Resources, metaclass=abc.ABCMeta):

    """This is the base class for AWS resources."""

    def __init__(self, facade, scope: dict):
        """
        :param scope: The scope holds the scope in which the resource is located. This usually means at least a region,
                      but can also contain a VPC id, an owner id, etc. It should be used when fetching the data through
                      the facade.
        """
        
        self.scope = scope
        self.facade = facade


class AWSCompositeResources(AWSResources, CompositeResources, metaclass=abc.ABCMeta):

    """This class represents a collection of AWSResources. Classes extending AWSCompositeResources should define a
    "_children" attribute which consists of a list of tuples describing the children. The tuples are expected to
    respect the following format: (<child_class>, <child_name>). The child_name is used by indicates the name under
    which the child will be stored in the parent object.
    """

    async def _fetch_children_of_all_resources(self, resources: dict, scopes: dict):
        """ This method iterates through a collection of resources and fetches all children of each resource, in a
        concurrent way.

        :param resources: list of (composite) resources
        :param scopes: dict that maps resource parent keys to scopes (dict) that should be used to retrieve children
        of each resource.
        """
        if len(resources) == 0:
            return

        tasks = {
            asyncio.ensure_future(
                self._fetch_children(resource_parent=resource_parent, scope=scopes[resource_parent_key])
            ) for (resource_parent_key, resource_parent) in resources.items()
        }
        await asyncio.wait(tasks)

    async def _fetch_children(self, resource_parent: object, scope: dict):
        """This method fetches all children of a given resource (the so called 'resource_parent') by calling fetch_all
        method on each child defined in '_children' and then stores the fetched resources in `resource_parent` under
        the key associated with the child. It also creates a "<child_name>_count" entry for each child.

        :param resource_parent: The resource in which the children will be stored.
        :param scope: The scope passed to the children constructors.
        """

        children = [(child_class(self.facade, scope), child_name) for (child_class, child_name) in self._children]
        # Fetch all children concurrently:
        await asyncio.wait(
            {asyncio.ensure_future(child.fetch_all()) for (child, _) in children}
        )
        # Update parent content:
        for child, child_name in children:
            if resource_parent.get(child_name) is None:
                resource_parent[child_name] = {}

            resource_parent[child_name].update(child)
            resource_parent[child_name + '_count'] = len(child)

