"""This module provides implementations for Resources and CompositeResources for Azure."""

import abc
import asyncio

from ScoutSuite.providers.base.configs.resources import Resources, CompositeResources
from ScoutSuite.providers.azure.facade.base import AzureFacade


class AzureResources(Resources, metaclass=abc.ABCMeta):

    """This is the base class for Azure resources."""

    def __init__(self, facade: AzureFacade, scope: dict = None):
        """
        :param scope: The scope holds the scope in which the resource is located. This could be a resource group name or any other
                      resource parent name. For example, scope of a SQL database would be {'resource_group_name': 'groupX', 'server_name': 'serverY'}.
                      This scope will be used when fetching data through the facade.
        """

        self.scope = scope
        self.facade = facade


class AzureCompositeResources(AzureResources, CompositeResources, metaclass=abc.ABCMeta):

    """This class represents a collection of composite Resources (resources that include nested resources referred as
    their children). Classes extending AzureCompositeResources have to define a '_children' attribute which consists of
    a list of tuples describing the children. The tuples are expected to respect the following format:
    (<child_class>, <child_name>). 'child_name' is used to indicate the name under which the child resources will be
    stored in the parent object.
    """

    pass
