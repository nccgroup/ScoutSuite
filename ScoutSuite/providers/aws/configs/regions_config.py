# -*- coding: utf-8 -*-
from ScoutSuite.providers.base.configs.resources import Resources
from ScoutSuite.providers.aws.facade.facade import AWSFacade
import abc


class Regions(Resources):
    def __init__(self, service):
        self._service = service

    async def fetch_all(self, chosen_regions=None, partition_name='aws'):
        # TODO: Should be injected
        facade = AWSFacade()

        self['regions'] = {}
        for region in await facade.build_region_list(self._service, chosen_regions, partition_name):
            self['regions'][region] = {}

        self['regions_count'] = len(self['regions'])


class ScopedResources(Resources):
    async def fetch_all(self, scope):
        for raw_resource in await self.get_resources_in_scope(scope):
            name, ressource = self.parse_resource(raw_resource)
            self[name] = ressource

        self.count = len(self)
        return self

    @abc.abstractclassmethod
    def parse_resource(self, resource):
        raise NotImplementedError()

    @abc.abstractclassmethod
    async def get_resources_in_scope(self, region):
        raise NotImplementedError()
