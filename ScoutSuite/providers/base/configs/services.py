# -*- coding: utf-8 -*-

from opinel.utils.console import printError, printException, printDebug
from opinel.utils.aws import get_aws_account_id, get_partition_name

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
                    method_args = {}
                    method_args['credentials'] = credentials
                    method_args['regions'] = regions

                    if self._is_provider('aws'):
                        if service != 'iam':
                            method_args['partition_name'] = get_partition_name(credentials)

                    service_config.fetch_all(**method_args)
                    if hasattr(service_config, 'finalize'):
                        service_config.finalize()
                else:
                    printDebug('No method to fetch service %s.' % service)
            except Exception as e:
                printError('Error: could not fetch %s configuration.' % service)
                printException(e)

    # TODO is this ever called?
    # def postprocessing(self):
    #     pass
