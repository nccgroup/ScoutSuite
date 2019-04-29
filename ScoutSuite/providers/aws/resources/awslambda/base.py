from ScoutSuite.providers.aws.facade.base import AWSFacade
from ScoutSuite.providers.aws.resources.regions import Regions
from ScoutSuite.providers.aws.resources.base import AWSResources


class Functions(AWSResources):
    def __init__(self, facade: AWSFacade, region: str):
        super(Functions, self).__init__(facade)
        self.region = region

    async def fetch_all(self):
        raw_functions = await self.facade.awslambda.get_functions(self.region)
        for raw_function in raw_functions:
            name, resource = self._parse_function(raw_function)
            self[name] = resource

    def _parse_function(self, raw_function):
        raw_function['name'] = raw_function.pop('FunctionName')
        return raw_function['name'], raw_function


class Lambdas(Regions):
    _children = [
        (Functions, 'functions')
    ]

    def __init__(self, facade: AWSFacade):
        super(Lambdas, self).__init__('lambda', facade)
