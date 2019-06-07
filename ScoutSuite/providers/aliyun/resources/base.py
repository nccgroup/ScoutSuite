"""This module provides implementations for Resources and CompositeResources for Aliyun."""

import abc

from ScoutSuite.providers.base.resources.base import Resources, CompositeResources


class AliyunResources(Resources, metaclass=abc.ABCMeta):
    """This is the base class for Aliyun resources."""

    pass


class AliyunCompositeResources(AliyunResources, CompositeResources, metaclass=abc.ABCMeta):
    """This class represents a collection of composite Resources (resources that include nested resources referred as
    their children). Classes extending AliyunCompositeResources have to define a '_children' attribute which consists of
    a list of tuples describing the children. The tuples are expected to respect the following format:
    (<child_class>, <child_name>). 'child_name' is used to indicate the name under which the child resources will be
    stored in the parent object.
    """

    pass
