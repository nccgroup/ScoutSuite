"""
This module provides some abstract classes for representing a hierarchical structure.
Especially since all cloud providers (AWS, Azure and GCP for now) organize their resources (virtual machines,
databases, load balancers, user accounts and so on...) with some kind of hierarchy, these classes may be
used to reflect that.
"""

import abc
import asyncio


class Resources(dict, metaclass=abc.ABCMeta):

    """This is the base class of a hierarchical structure. Everything is basically `Resources`.
    It stores in its internal dictionary instances of a given type of resources, with instance ids as keys and
    instance configurations (which store other nested resources) as values.
    """

    def __init__(self, service_facade):
        self.facade = service_facade

        super().__init__()

    @abc.abstractmethod
    async def fetch_all(self, **kwargs):
        """Fetches, parses and stores instances of a given type of resources from a cloud provider API.

        :param kwargs:
        :return:
        """
        raise NotImplementedError()


class CompositeResources(Resources, metaclass=abc.ABCMeta):

    """This class represents a node in the hierarchical structure. As inherited from `Resources`, it still \
    stores instances of a given type of resources internally but also stores some kind of nested resources \
    referred to as its 'children'.
    """

    @property
    @abc.abstractmethod
    def _children(self):
        """A class that inherits from 'CompositeResources' should define a private '_children' attribute, typically a
        list of `Resources` classes. That is enforced by this abstract property.
        """
        raise NotImplementedError

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
                self._fetch_children(
                    resource_parent=resource_parent, scope=scopes[resource_parent_key])
            ) for (resource_parent_key, resource_parent) in resources.items()
        }
        await asyncio.wait(tasks)

    async def _fetch_children(self, resource_parent: object, scope: dict = {}):
        """This method fetches all children of a given resource (the so called 'resource_parent') by calling fetch_all
        method on each child defined in '_children' and then stores the fetched resources in `resource_parent` under
        the key associated with the child. It also creates a "<child_name>_count" entry for each child.

        :param resource_parent: The resource in which the children will be stored.
        :param scope: The scope passed to the children constructors.
        """
        children = [(child_class(self.facade, **scope), child_name)
                    for (child_class, child_name) in self._children]
        # Fetch all children concurrently:
        await asyncio.wait(
            {asyncio.ensure_future(child.fetch_all())
             for (child, _) in children}
        )
        # Update parent content:
        for child, child_name in children:
            if child_name is None:
                resource_parent.update(child)
            else:
                if resource_parent.get(child_name) is None:
                    resource_parent[child_name] = {}
                    resource_parent[child_name + '_count'] = 0

                resource_parent[child_name].update(child)
                resource_parent[child_name + '_count'] += len(child)
