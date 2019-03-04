import abc

from ScoutSuite.providers.base.configs.resources import CompositeResources


class AzureCompositeResources(CompositeResources, metaclass=abc.ABCMeta):

    async def _fetch_children(self, parent, **kwargs):
        for child_class in self._children:
            child = child_class(**kwargs)
            await child.fetch_all()
            parent.update(child)
