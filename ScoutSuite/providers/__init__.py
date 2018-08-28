# -*- coding: utf-8 -*-

import sys

from ScoutSuite.providers.aws.provider import AWSProvider
from ScoutSuite.providers.gcp.provider import GCPProvider

providers_dict = {'aws': 'AWSProvider',
                  'gcp': 'GCPProvider'}

def get_provider(provider, profile, report_dir=None, timestamp=None, services=[], skipped_services=[], thread_config=4):
    """
    Returns an instance of the requested provider.

    :param provider: a string indicating the provider
    :return: a child instance of the BaseProvider class or None if no object implemented
    """

    provider_class = providers_dict.get(provider)
    provider_object = getattr(sys.modules[__name__], provider_class)
    provider_instance = provider_object(profile, report_dir, timestamp, services, skipped_services, thread_config)

    return provider_instance
