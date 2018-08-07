# -*- coding: utf-8 -*-

import sys

from ScoutSuite.providers.aws.aws_provider import AWSProvider

providers_dict = {'aws': 'AWSProvider'}


def get_provider(provider):
    """
    Returns an instance of the requested provider.

    :param provider: a string indicating the provider
    :return: a child instance of the BaseProvider class or None if no object implemented
    """

    provider_class = providers_dict.get(provider)
    provider_object = getattr(sys.modules[__name__], provider_class)
    provider_instance = provider_object()

    return provider_instance
