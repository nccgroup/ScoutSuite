# -*- coding: utf-8 -*-
from ScoutSuite.providers.base.configs.resource_config import ResourceConfig
from ScoutSuite.providers.aws.configs.regions_config import RegionsConfig
from ScoutSuite.providers.aws.aws_facade import AwsFacade
from opinel.utils.aws import build_region_list

class LambdaServiceConfig(RegionsConfig):
    def __init__(self):
        super(LambdaServiceConfig, self).__init__('lambda')

    async def fetch_all(self, credentials, regions=None, partition_name='aws', targets=None):
        await super(LambdaServiceConfig, self).fetch_all(
            chosen_regions=regions, 
            partition_name=partition_name
        )

        for region in self['regions']:
            functions = LambdasConfig()
            await functions.fetch_all(region=region)
            self['regions'][region] = functions
        

class LambdasConfig(ResourceConfig):
    async def fetch_all(self, region):
        # TODO: Should be injected
        facade = AwsFacade()
        
        functions = {}
        for raw_function in facade.get_lambda_functions(region):
            name, function = self.parse_function(raw_function)
            functions[name] = function

        self['functions_count'] = len(functions))        
        self.setdefault('functions', functions)

    @staticmethod
    def parse_function(function):
        function['name'] = function.pop('FunctionName')
        return (function['name'], function)
