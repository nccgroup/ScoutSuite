import abc

from ScoutSuite.providers.bamboohr.resources.base import BambooHRResources
from ScoutSuite.providers.bamboohr.facade.base import BambooHRFacade

class Employees(BambooHRResources, metaclass=abc.ABCMeta):
    def __init__(self, facade):
        super(Employees, self).__init__(facade)

    async def fetch_all(self, **kwargs):
        self["directory"] = await self.facade.fetch_all()
        self["employees_count"] = len(self["directory"])