import abc
import asyncio

from ScoutSuite.providers.base.configs.resources import CompositeResources


class AzureCompositeResources(CompositeResources, metaclass=abc.ABCMeta):

    async def _fetch_children(self, parent, **kwargs):
        children = [child_class(**kwargs) for child_class in self._children]
        # fetch all children concurrently:
        await asyncio.wait({asyncio.create_task(child.fetch_all()) for child in children})
        # update parent content:
        for child in children:
            parent.update(child)
