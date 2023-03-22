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

        """
        调用 _children 中定义的每个子类的 fetch_all 方法来获取给定资源的所有子资源，并将获取的资源存储在 resource_parent 中与子资源关联的键下。
        它还为每个子资源创建一个 "<child_name>_count" 条目。
        负责创建一个元组列表，其中每个元组包含一个子类的实例和该子类的名称。列表是通过迭代 CompositeResources 类的 _children 属性创建的。
        child_class 是 Resources 子类的一个实例，child_name 是表示子类名称的字符串。然后使用 children 列表并发地获取所有子资源。
        在 children 列表中调用 fetch_all 方法，并将结果存储在 resource_parent 字典中。最后，使用获取的资源更新 resource_parent 字典。
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
