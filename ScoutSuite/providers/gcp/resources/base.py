"""This module provides implementations for CompositeResources for GCP."""

from ScoutSuite.providers.base.resources.base import CompositeResources


class GCPCompositeResources(CompositeResources):

    """This class represents a collection of Resources from GCP. Classes extending GCPCompositeResources should define a
    "_children" attribute which consists of a list of tuples describing the children. The tuples are expected to
    respect the following format: (<child_class>, <child_name>). The child_name is used by indicates the name under
    which the child will be stored in the parent object.
    """
    
    pass
