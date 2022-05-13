from ScoutSuite.providers.base.resources.base import Resources
from ScoutSuite.providers.gcp.facade.base import GCPFacade


class FunctionsV1(Resources):
    def __init__(self, facade: GCPFacade, project_id: str):
        super().__init__(facade)
        self.project_id = project_id

    async def fetch_all(self):
        raw_functions = await self.facade.functions.get_functions_v1(self.project_id)
        for raw_function in raw_functions:
            function_id, function = self._parse_function(raw_function)
            self[function_id] = function

    def _parse_function(self, raw_function):
        print()
        print(raw_function)
        return None, None
