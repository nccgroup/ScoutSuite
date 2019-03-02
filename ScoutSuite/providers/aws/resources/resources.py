from ScoutSuite.providers.base.configs.resources import Resources, CompositeResources
from ScoutSuite.providers.aws.facade.facade import AWSFacade
import abc


class AWSResources(Resources, metaclass=abc.ABCMeta):
    def __init__(self, scope):
        self.scope = scope
        self.facade = AWSFacade()


class AWSCompositeResources(AWSResources, CompositeResources, metaclass=abc.ABCMeta):
    async def _fetch_children(self, parent, **kwargs):
        for child_class, key in self.children:
            child = child_class(**kwargs)
            await child.fetch_all()
            if parent.get(key) is None:
                parent[key] = {}
            parent[key].update(child)
            parent[key + '_count'] = len(child)