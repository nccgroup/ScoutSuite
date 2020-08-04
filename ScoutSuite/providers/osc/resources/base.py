
import abc

from ScoutSuite.providers.base.resources.base import Resources, CompositeResources


class OSCResources(Resources, metaclass=abc.ABCMeta):
    """This is the base class for OSC resources."""
    pass


class OSCCompositeResources(OSCResources, CompositeResources, metaclass=abc.ABCMeta):
    pass