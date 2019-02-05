# -*- coding: utf-8 -*-

# Python2 vs Python3
try:
    from Queue import Queue
except ImportError:
    from queue import Queue

from ScoutSuite.providers.base.configs.base import BaseConfig


class AzureBaseConfig(BaseConfig):

    def __init__(self, thread_config=4, **kwargs):

        super(AzureBaseConfig, self).__init__(thread_config)

    def _is_provider(self, provider_name):
        return provider_name == 'azure'

    def _get_method(self, api_client, target_type, list_method_name):
        """
        Gets the appropriate method, required as each provider may have particularities

        :return:
        """

        target = getattr(api_client, target_type)
        method = getattr(target, list_method_name)

        return method

    def _get_targets(self, response_attribute, api_client, method, list_params, ignore_list_error):
        """
        Fetch the targets, required as each provider may have particularities

        :return:
        """

        targets = []
        response = method(**list_params)
        for i in response:
            targets.append(i)

        return targets
