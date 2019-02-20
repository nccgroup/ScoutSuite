# -*- coding: utf-8 -*-
from ScoutSuite.providers.base.configs.resource_config import ResourceConfig
from ScoutSuite.providers.aws.aws_facade import AwsFacade


class RegionsConfig(ResourceConfig):

    def __init__(self, service, child_config_type):
        self._service = service
        self._child_config_type = child_config_type

    async def fetch_all(self, credentials, regions=None, partition_name='aws', targets=None):
        # TODO: Should be injected
        facade = AwsFacade()

        for region in await facade.build_region_list(self._service, regions, partition_name):
            child = self._child_config_type()
            await child.fetch_all(credentials, region, partition_name, None)
            self.setdefault(region, child)
