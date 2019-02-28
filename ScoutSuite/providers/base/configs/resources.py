# -*- coding: utf-8 -*-
"""
This module provides some abstract classes for representing a hierarchical structure.
Especially since all cloud providers (AWS, Azure and GCP for now) organize their resources (virtual machines,
databases, load balancers, user accounts and so on...) with some kind of hierarchy, these classes may be
used to reflect that.
"""

import abc


class Resources(dict, metaclass=abc.ABCMeta):

    """
    This is the base class of a hierarchical structure. Everything is basically `Resources`.
    It stores in its internal dictionary instances of a given type of resources, with instance ids as keys and
    instance configurations (which store other nested resources) as values.
    """

    @abc.abstractmethod
    async def fetch_all(self, **kwargs):
        """Fetches, parses and stores instances of a given type of resources from a cloud provider API.

        :param kwargs:
        :return:
        """
        raise NotImplementedError()


class CompositeResources(Resources, metaclass=abc.ABCMeta):

    """
    This class represents a node in the hierarchical structure.
    As inherited from `Resources`, it still stores instances of a given type of resources internally but
    also store some kind of nested resources referred as its 'children'.
    """

    @property
    @abc.abstractmethod
    def children(self):
        """A class that inherits from 'CompositeResources' should define a 'children' attribute, typically a list of
         `Resources` classes. That is enforced by this abstract property.

        :return:
        """
        raise NotImplementedError

    @abc.abstractmethod
    async def fetch_children(self, **kwargs):
        """Fetches, parses and stores instances of nested resources included in a `CompositeResources` and defined
        in the 'children' attribute.

        :param kwargs:
        :return:
        """
        raise NotImplementedError
