# -*- coding: utf-8 -*-

from ScoutSuite.providers.azure.configs.base import AzureBaseConfig
from ScoutSuite.providers.azure.utils import get_resource_group_name


class RedisCacheConfig(AzureBaseConfig):
    targets = (
        ('redis', 'Redis Caches', 'list', {}, False),
    )

    def __init__(self, thread_config):

        self.caches = {}
        self.caches_count = 0

        super(RedisCacheConfig, self).__init__(thread_config)

    def parse_redis(self, cache, params):
        cache_dict = {}

        cache_dict['id'] = self.get_non_provider_id(cache.id)
        cache_dict['name'] = cache.name
        cache_dict['public_access_allowed'] = self._is_public_access_allowed(cache)

        self.caches[cache_dict['id']] = cache_dict

    def _is_public_access_allowed(self, cache):
        return len(cache.firewall_rules) == 0

    def _get_targets(self, response_attribute, api_client, method, list_params, ignore_list_error):
        if response_attribute == "Redis Caches":
            return self._get_redis_caches(api_client, method, list_params)
        else:
            return super(RedisCacheConfig, self)._get_targets(response_attribute, api_client, method,
                                                                   list_params, ignore_list_error)

    def _get_redis_caches(self, api_client, method, list_params):
        redis_caches = []
        redis_caches_raw = method(**list_params)
        for redis_cache in redis_caches_raw:
            resource_group_name = get_resource_group_name(redis_cache.id)
            setattr(redis_cache, "firewall_rules",
                    list(api_client.firewall_rules.list_by_redis_resource(resource_group_name, redis_cache.name)))
            redis_caches.append(redis_cache)

        return redis_caches
