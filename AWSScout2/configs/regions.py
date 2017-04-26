# -*- coding: utf-8 -*-
"""
Base classes and functions for region-specific services
"""

import re

from threading import Event, Thread
# Python2 vs Python3
try:
    from Queue import Queue
except ImportError:
    from queue import Queue

from opinel.utils.aws import build_region_list, connect_service, handle_truncated_response
from opinel.utils.console import printException, printInfo

from AWSScout2.utils import format_service_name
from AWSScout2.configs.base import GlobalConfig
from AWSScout2.output.console import FetchStatusLogger





########################################
# Globals
########################################

api_clients = dict()

first_cap_re = re.compile('(.)([A-Z][a-z]+)')
all_caps_re = re.compile('([a-z0-9])([A-Z])')


########################################
# RegionalServiceConfig
########################################

class RegionalServiceConfig(object):
    """
    Single service configuration for non-global services

    :ivar regions:                      Dictionary of regions
    :ivar service:                      Name of the service
    """

    def __init__(self):
        self.regions = {}
        self.service = type(self).__name__.replace('Config', '').lower() # TODO: use regex with EOS instead of plain replace

    def init_region_config(self, region):
        """
        Initialize the region's configuration

        :param region:                  Name of the region
        """
        self.regions[region] = self.region_config_class()


    def fetch_all(self, credentials, regions = [], partition_name = 'aws', targets = None):
        """
        Fetch all the SNS configuration supported by Scout2

        :param credentials:             F
        :param service:                 Name of the service
        :param regions:                 Name of regions to fetch data from
        :param partition_name:          AWS partition to connect to
        :param targets:                 Type of resources to be fetched; defaults to all.

        """
        # Initialize targets
        if not targets:
            targets = type(self).targets
        printInfo('Fetching %s config...' % format_service_name(self.service))
        self.fetchstatuslogger = FetchStatusLogger(targets, True)
        api_service = 'ec2' if self.service.lower() == 'vpc' else self.service.lower()
        # Init regions
        regions = build_region_list(api_service, regions, partition_name) # TODO: move this code within this class
        self.fetchstatuslogger.counts['regions']['discovered'] = len(regions)
        # Threading to fetch & parse resources (queue consumer)
        q = self._init_threading(self._fetch_target, {}, 20)
        # Threading to list resources (queue feeder)
        qr = self._init_threading(self._fetch_region, {'api_service': api_service, 'credentials': credentials, 'q': q, 'targets': targets}, 10)
        # Go
        for region in regions:
            qr.put(region)
        # Join
        qr.join()
        q.join()
        # Show completion and force newline
        self.fetchstatuslogger.show(True)

    def _init_threading(self, function, params={}, num_threads=10):
            # Init queue and threads
            q = Queue(maxsize=0) # TODO: find something appropriate
            if not num_threads:
                num_threads = len(targets)
            for i in range(num_threads):
                worker = Thread(target=function, args=(q, params))
                worker.setDaemon(True)
                worker.start()
            return q

    def _fetch_region(self, q, params):
        global api_clients
        try:
            while True:
                try:
                    region = q.get()
                    self.init_region_config(region)
                    api_client = connect_service(params['api_service'], params['credentials'], region)
                    api_clients[region] = api_client
                    self.regions[region].fetch_all(api_client, self.fetchstatuslogger, params['q'], params['targets'])
                    self.fetchstatuslogger.counts['regions']['fetched'] += 1
                except Exception as e:
                    printException(e)
                finally:
                    q.task_done()
        except Exception as e:
            printException(e)
            pass

    def _fetch_target(self, q, params):
        try:
            while True:
                try:
                    method, region, target = q.get()
                    method(params, region, target)
                    target = method.__name__.replace('parse_', '') + 's'
                    self.fetchstatuslogger.counts[target]['fetched'] += 1
                    self.fetchstatuslogger.show()
                except Exception as e:
                    printException(e)
                finally:
                    q.task_done()
        except Exception as e:
            printException(e)
            pass

    def finalize(self):
        for t in self.fetchstatuslogger.counts:
            setattr(self, '%s_count' % t, self.fetchstatuslogger.counts[t]['fetched'])
        delattr(self, 'fetchstatuslogger')
        for r in self.regions:
            if hasattr(self.regions[r], 'fetchstatuslogger'):
                delattr(self.regions[r], 'fetchstatuslogger')



########################################
# RegionConfig
########################################

class RegionConfig(GlobalConfig):
    """
    Base class for ...
    """

    def __init__(self, region_name):
        self.region = region_name

    def fetch_all(self, api_client, fetchstatuslogger, q, targets):
        self.fetchstatuslogger = fetchstatuslogger
        if targets != None:
            # Ensure targets is a tuple
            if type(targets) != list and type(targets) != tuple:
                targets = tuple(targets,)
            elif type(targets) != tuple:
                targets = tuple(targets)
#        else:
#            targets = tuple(['%s' % method.replace('fetch_','').title() for method in methods])
        for target in targets:
            self._fetch_targets(api_client, q, target, {})


    def _fetch_targets(self, api_client, q, target, list_params):
        # Handle & format the target type
        target_type, response_attribute, list_method_name, ignore_list_error = target
        list_method = getattr(api_client, list_method_name)
        try:
            targets = handle_truncated_response(list_method, list_params, [response_attribute])[response_attribute]
        except Exception as e:
            if not ignore_list_error:
                printException(e)
            targets = []
        setattr(self, '%s_count' % target_type, len(targets))
        self.fetchstatuslogger.counts[target_type]['discovered'] += len(targets)
        region = api_client._client_config.region_name
        # Queue resources
        for target in targets:
            callback = getattr(self, 'parse_%s' % target_type[0:-1])
            if q:
                # Add to the queue
                q.put((callback, region, target))
