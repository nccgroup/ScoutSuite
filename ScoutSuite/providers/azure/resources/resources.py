import abc
import asyncio

from ScoutSuite.providers.base.configs.resources import CompositeResources


# TODO: add docstrings.
class AzureCompositeResources(CompositeResources, metaclass=abc.ABCMeta):

    async def _fetch_children(self, parent, **kwargs):
        children = [(child_class(**kwargs), child_name) for (child_class, child_name) in self._children]
        # fetch all children concurrently:
        await asyncio.wait({asyncio.create_task(child.fetch_all()) for (child, _) in children})
        # update parent content:
        for child, name in children:
            if name:
                parent[name] = child
            else:
                parent.update(child)
