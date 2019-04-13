"""This module provides implementations for Resources and CompositeResources for AWS."""

import abc
import asyncio

from ScoutSuite.providers.base.configs.resources import Resources, CompositeResources



class AWSResources(Resources, metaclass=abc.ABCMeta):

    """This is the base class for AWS resources."""

    def __init__(self, facade, scope: dict):
        """
        :param scope: The scope holds the scope in which the resource is located. This usually means at least a region,
                      but can also contain a VPC id, an owner id, etc. It should be used when fetching the data through
                      the facade.
        """
        
        self.scope = scope
        self.facade = facade


class AWSCompositeResources(AWSResources, CompositeResources, metaclass=abc.ABCMeta):

    """This class represents a collection of AWSResources. Classes extending AWSCompositeResources should define a
    "_children" attribute which consists of a list of tuples describing the children. The tuples are expected to
    respect the following format: (<child_class>, <child_name>). The child_name is used by indicates the name under
    which the child will be stored in the parent object.

    """
    
    pass