# -*- coding: utf-8 -*-
from ScoutSuite.providers.aws.resources.resources import Regions, AWSSimpleResources
from ScoutSuite.providers.aws.facade.facade import AWSFacade
from opinel.utils.aws import build_region_list

class RegionalLambdas(AWSSimpleResources):
    async def get_resources_from_api(self):
        return self.facade.awslambda.get_functions(self.scope['region'])
        
    def parse_resource(self, raw_function):
        raw_function['name'] = raw_function.pop('FunctionName')
        return (raw_function['name'], raw_function)

    @staticmethod
    def parse_function(function):
        function['name'] = function.pop('FunctionName')
        return (function['name'], function)


class Lambdas(Regions):
    children = [
        (RegionalLambdas, 'functions')
    ]

    def __init__(self):
        super(Lambdas, self).__init__('lambda')

    # TODO: Remove the credentials parameter. We had to keep it for compatibility
    async def fetch_all(self, credentials=None, regions=None, partition_name='aws'):
        await super(Lambdas, self).fetch_all(credentials, regions, partition_name)