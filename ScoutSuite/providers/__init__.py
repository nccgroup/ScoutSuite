# -*- coding: utf-8 -*-

import sys

from ScoutSuite.providers.aws.provider import AWSProvider
from ScoutSuite.providers.gcp.provider import GCPProvider
from ScoutSuite.providers.azure.provider import AzureProvider

providers_dict = {'aws': 'AWSProvider',
                  'gcp': 'GCPProvider',
                  'azure': 'AzureProvider'}

def get_provider(provider,
                 profile=None,
                 project_id=None, folder_id=None, organization_id=None,
                 report_dir=None, timestamp=None, services=None, skipped_services=None, thread_config=4, **kwargs):
    """
    Returns an instance of the requested provider.

    :param provider: a string indicating the provider
    :return: a child instance of the BaseProvider class or None if no object implemented
    """
    services = [] if services is None else services
    skipped_services = [] if skipped_services is None else skipped_services

    provider_class = providers_dict.get(provider)
    provider_object = getattr(sys.modules[__name__], provider_class)
    provider_instance = provider_object(profile=profile,
                                        project_id=project_id,
                                        folder_id=folder_id,
                                        organization_id=organization_id,
                                        report_dir=report_dir,
                                        timestamp=timestamp,
                                        services=services,
                                        skipped_services=skipped_services,
                                        thread_config=thread_config,
                                        **kwargs)

    return provider_instance
