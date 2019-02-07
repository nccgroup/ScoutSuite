# -*- coding: utf-8 -*-

from opinel.utils.console import printException

from google.cloud import storage
from google.cloud import logging as stackdriver_logging
from google.cloud import monitoring_v3
from google.cloud import container_v1

from googleapiclient import discovery

import logging

def gcp_connect_service(service, credentials=None, region_name=None):

    logging.getLogger('googleapiclient.discovery_cache').setLevel(logging.ERROR)
    # Set logging level to error for GCP services as otherwise generates a lot of warnings
    logging.getLogger().setLevel(logging.ERROR)

    try:

        if service == 'cloudresourcemanager':
            return discovery.build('cloudresourcemanager', 'v1', cache_discovery=False, cache=MemoryCache())

        elif service == 'cloudresourcemanager-v2':
            return discovery.build('cloudresourcemanager', 'v2', cache_discovery=False, cache=MemoryCache())

        elif service == 'cloudstorage':
            # return storage.Client()
            return storage.Client(project='placeholder')  # need a project value to instantiate the client event though
                                                          # it won't be used afterwards

        elif service == 'cloudsql':
            return discovery.build('sqladmin', 'v1beta4', cache_discovery=False, cache=MemoryCache())

        elif service == 'iam':
            return discovery.build('iam', 'v1', cache_discovery=False, cache=MemoryCache())

        if service == 'stackdriverlogging':
            # return stackdriver_logging.LoggingServiceV2Client()
            return stackdriver_logging.Client(project='placeholder')  # need a project value to instantiate the client
                                                                      # event though it won't be used afterwards

        if service == 'stackdrivermonitoring':
            return monitoring_v3.MetricServiceClient()

        elif service == 'computeengine':
            return discovery.build('compute', 'v1', cache_discovery=False, cache=MemoryCache())

        elif service == 'kubernetesengine':
            return container_v1.ClusterManagerClient()

        else:
            printException('Service %s not supported' % service)
            return None

    except Exception as e:
        printException(e)
        return None


class MemoryCache:
    """
    Workaround https://github.com/googleapis/google-api-python-client/issues/325#issuecomment-274349841
    """
    _CACHE = {}

    def get(self, url):
        return MemoryCache._CACHE.get(url)

    def set(self, url, content):
        MemoryCache._CACHE[url] = content