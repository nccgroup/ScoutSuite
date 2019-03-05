# -*- coding: utf-8 -*-

from ScoutSuite.core.console import print_error, print_exception, print_debug
from ScoutSuite.providers.aws.aws import get_partition_name


class BaseServicesConfig(object):

    def __init__(self, metadata=None, thread_config=4):
        pass

    def _is_provider(self, provider_name):
        return False

    def fetch(self, credentials, services=None, regions=None):
        services = [] if services is None else services
        regions = [] if regions is None else regions
        for service in vars(self):
            try:
                # skip services
                if services != [] and service not in services:
                    continue
                service_config = getattr(self, service)
                # call fetch method for the service
                if 'fetch_all' in dir(service_config):
                    method_args = {'credentials': credentials, 'regions': regions}

                    if self._is_provider('aws'):
                        if service != 'iam':
                            method_args['partition_name'] = get_partition_name(credentials)

                    service_config.fetch_all(**method_args)
                    if hasattr(service_config, 'finalize'):
                        service_config.finalize()
                else:
                    print_debug('No method to fetch service %s.' % service)
            except Exception as e:
                print_error('Error: could not fetch %s configuration.' % service)
                print_exception(e)
