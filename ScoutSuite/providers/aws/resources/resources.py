"""This module provides implementations for Resources and CompositeResources for AWS."""

import abc
import asyncio

from ScoutSuite.providers.base.configs.resources import Resources, CompositeResources
from ScoutSuite.providers.aws.facade.facade import AWSFacade


class AWSResources(Resources, metaclass=abc.ABCMeta):

    """This is the base class for AWS resources."""

    def __init__(self, facade, scope: dict):
        """
        :param scope: The scope holds the scope in which the resource is located. This usually means \
                      at least a region, but can also contain a VPC id, an owner id, etc. It should be \
                      used when fetching the data through the facade.
        """
        
        self.scope = scope
        self.facade = facade


class AWSCompositeResources(AWSResources, CompositeResources, metaclass=abc.ABCMeta):

    """This class represents a collection of AWSResources. Classes extending AWSCompositeResources should \
    define a "_children" attribute which consists of a list of tuples describing the children. The tuples \
    are expected to respect the following format: (<child_class>, <child_name>). The child_name is used by \
    indicates the name under which the child will be stored in the parent object.
    """
        
    async def _fetch_children(self, parent: object, scope: dict):
        """This method calls fetch_all on each child defined in "_children" and stores the fetched resources \
        in the parent under the key associated with the child. It also creates a "<child_name>_count" entry \
        for each child.

        :param parent: The object in which the children should be stored
        :param scope: The scope passed to the children constructors
        """

        children = [(child_class(self.facade, scope), child_name) for (child_class, child_name) in self._children]
        # fetch all children concurrently:
        await asyncio.wait({asyncio.ensure_future(child.fetch_all()) for (child, _) in children})
        # update parent content:
        for child, child_name in children:
            if parent.get(child_name) is None:
                parent[child_name] = {}

            parent[child_name].update(child)
            parent[child_name + '_count'] = len(child)

