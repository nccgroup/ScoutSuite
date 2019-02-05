# -*- coding: utf-8 -*-

# Python2 vs Python3
try:
    from Queue import Queue
except ImportError:
    from queue import Queue

from ScoutSuite.providers.base.configs.base import BaseConfig

from opinel.utils.aws import handle_truncated_response


class AWSBaseConfig(BaseConfig):

    def _is_provider(self, provider_name):
        return provider_name == 'aws'

    def _get_method(self, api_client, target_type, list_method_name):
        """
        Gets the appropriate method, required as each provider may have particularities

        :return:
        """

        method = getattr(api_client, list_method_name)

        return method

    def _get_targets(self, response_attribute, api_client, method, list_params, ignore_list_error):
        """
        Fetch the targets, required as each provider may have particularities

        :return:
        """

        if type(list_params) != list:
            list_params = [list_params]

        targets = []
        for lp in list_params:
            targets += handle_truncated_response(method, lp, [response_attribute])[response_attribute]

        return targets
