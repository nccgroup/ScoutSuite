import asyncio
from ScoutSuite.providers.base.configs.resources import CompositeResources

class GCPCompositeResources(CompositeResources):
    async def _fetch_children(self, parent, **kwargs):
        children = [(child_class(**kwargs), child_name) for (child_class, child_name) in self._children]
        await asyncio.wait({asyncio.ensure_future(child.fetch_all()) for (child, _) in children})
        for child, child_name in children:
            parent[child_name] = child
            parent[child_name + '_count'] = len(child)