from ScoutSuite.providers.azure.facade.base import AzureFacade
from ScoutSuite.providers.azure.utils import get_resource_group_name
from ScoutSuite.providers.base.configs.resources import Resources
from ScoutSuite.providers.utils import get_non_provider_id


class RedisCaches(Resources):

    def __init__(self, facade: AzureFacade):
        self.facade = facade

    async def fetch_all(self, credentials, **kwargs):
        self['caches'] = {}
        # The following loop could be parallelized in case of bottleneck:
        for raw_cache in await self.facade.rediscache.get_redis_caches():
            id, redis_cache = await self._parse_redis_cache(raw_cache)
            self['caches'][id] = redis_cache

        self['caches_count'] = len(self['caches'])

    async def _parse_redis_cache(self, cache):
        cache_dict = {}
        cache_dict['id'] = get_non_provider_id(cache.id)
        cache_dict['name'] = cache.name
        cache_dict['public_access_allowed'] = await self._is_public_access_allowed(cache)

        return cache_dict['id'], cache_dict

    async def _is_public_access_allowed(self, cache):
        firewall_rules = await self.facade.rediscache.get_redis_firewall_rules(
            get_resource_group_name(cache.id), cache.name)

        return len(firewall_rules) == 0
