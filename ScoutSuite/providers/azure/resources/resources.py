import abc

from ScoutSuite.providers.base.configs.resources import CompositeResources


# TODO: add docstrings.
class AzureCompositeResources(CompositeResources, metaclass=abc.ABCMeta):

    async def _fetch_children(self, parent, **kwargs):
        for child_class, name in self._children:
            child = child_class(**kwargs)
            await child.fetch_all()
            if name:
                parent[name] = child
            else:
                parent.update(child)
