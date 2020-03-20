"""This module provides implementations for Resources and CompositeResources for AWS."""

import abc

from ScoutSuite.providers.base.resources.base import Resources, CompositeResources


class AWSResources(Resources, metaclass=abc.ABCMeta):
    """This is the base class for AWS resources."""

    pass


class AWSCompositeResources(AWSResources, CompositeResources, metaclass=abc.ABCMeta):
    """This class represents a collection of AWSResources. Classes extending AWSCompositeResources should define a
    "_children" attribute which consists of a list of tuples describing the children. The tuples are expected to
    respect the following format: (<child_class>, <child_name>). The child_name is used by indicates the name under
    which the child will be stored in the parent object.
    """

    pass
