from ScoutSuite.providers.aws.facade.facade import AWSFacade
from ScoutSuite.providers.aws.resources.regions import Regions
from ScoutSuite.providers.aws.resources.resources import AWSResources


class Functions(AWSResources):
    async def fetch_all(self, **kwargs):
        raw_functions = await self.facade.awslambda.get_functions(self.scope['region'])
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
