# -*- coding: utf-8 -*-
from ScoutSuite.providers.base.configs.resource_config import ResourceConfig
from botocore.session import Session
from collections import Counter


class RegionsConfig(ResourceConfig):

    def __init__(self, service, child_config_type):
        self._service = service
        self._child_config_type = child_config_type

    async def fetch_all(self, credentials, regions=None, partition_name='aws', targets=None):
        for region in await self._build_region_list(regions, partition_name):
            child = self._child_config_type()
            await child.fetch_all(credentials, region, partition_name, None)
            self.setdefault(region, child)

    async def _build_region_list(self, chosen_regions=None, partition_name='aws'):
        service = 'ec2containerservice' if self._service == 'ecs' else self._service
        available_services = Session().get_available_services()

        if service not in available_services:
            raise Exception('Service ' + service + ' is not available.')

        regions = Session().get_available_regions(service, partition_name)

        if chosen_regions:
            return list((Counter(regions) & Counter(chosen_regions)).elements())
        else:
            return regions
