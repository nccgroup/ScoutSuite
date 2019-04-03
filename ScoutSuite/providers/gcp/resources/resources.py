"""This module provides implementations for CompositeResources for GCP."""

import asyncio
from ScoutSuite.providers.base.configs.resources import CompositeResources

class GCPCompositeResources(CompositeResources):

    """This class represents a collection of Resources from GCP. Classes extending GCPCompositeResources should define a
    "_children" attribute which consists of a list of tuples describing the children. The tuples are expected to
    respect the following format: (<child_class>, <child_name>). The child_name is used by indicates the name under
    which the child will be stored in the parent object.
    """

    async def _fetch_children(self, resource_parent: object, **kwargs):
        """This method fetches all children of a given resource (the so called 'resource_parent') by calling fetch_all
        method on each child defined in '_children' and then stores the fetched resources in `resource_parent` under
        the key associated with the child. It also creates a "<child_name>_count" entry for each child.

        :param resource_parent: The resource in which the children will be stored.
        :param kwargs: The arguments with which to build the child classes.
        """

        children = [(child_class(**kwargs), child_name) for (child_class, child_name) in self._children]
        await asyncio.wait({asyncio.ensure_future(child.fetch_all()) for (child, _) in children})
        for child, child_name in children:
            resource_parent[child_name] = child
            resource_parent[child_name + '_count'] = len(child)