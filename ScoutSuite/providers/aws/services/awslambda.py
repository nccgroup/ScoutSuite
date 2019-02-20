# -*- coding: utf-8 -*-
from ScoutSuite.providers.base.configs.resource_config import ResourceConfig
from ScoutSuite.providers.aws.configs.regions_config import RegionsConfig
from ScoutSuite.providers.aws.aws_facade import AwsFacade
from opinel.utils.aws import build_region_list

class LambdaServiceConfig(ResourceConfig):
    async def fetch_all(self, credentials, regions=None, partition_name='aws', targets=None):
        regions = RegionsConfig('lambda', LambdasConfig)
        await regions.fetch_all(credentials, regions, partition_name, None)
        self.setdefault('regions_count', len(regions))
        self.setdefault('regions', regions)

class LambdasConfig(ResourceConfig):
    async def fetch_all(self, credentials, region, partition_name='aws', targets=None):
        # TODO: Should be injected
        facade = AwsFacade()
        
        functions = {}
        for raw_function in facade.get_lambda_functions(region):
            name, function = self.parse_function(raw_function)
            functions[name] = function

        self.setdefault('functions_count', len(functions))        
        self.setdefault('functions', functions)

    @staticmethod
    def parse_function(function):
        function['name'] = function.pop('FunctionName')
        return (function['name'], function)
