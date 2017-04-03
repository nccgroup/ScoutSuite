# -*- coding: utf-8 -*-
"""
Base classes and functions for region-specific services
"""

from opinel.utils import printException, printInfo, manage_dictionary, connect_service, handle_truncated_response, build_region_list

from AWSScout2.utils import format_service_name
from AWSScout2.configs.base import GlobalConfig


# Import stock packages
import re
from hashlib import sha1


import sys
from threading import Event, Thread
# Python2 vs Python3
try:
    from Queue import Queue
except ImportError:
    from queue import Queue



########################################
# Globals
########################################

api_clients = dict()

status = None
regions = None
formatted_string = None

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
        global status, formatted_string
        # Initialize targets
        if not targets:
            targets = type(self).targets
        printInfo('Fetching %s config...' % format_service_name(self.service))
        counts = {}
        status = {'counts': {}, 'regions': [], 'regions_count': 0}
        formatted_string = None
        api_service = 'ec2' if self.service.lower() == 'vpc' else self.service.lower()
        # Init regions
        regions = build_region_list(api_service, regions, partition_name) # TODO: move this code within this class
        # TODO : skip multi regions for S3 because list bucket gets all buckets across regions (or overwrite fetch_all in S3 like for IAM)
        status['regions_count'] = len(regions)
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
        status_show(True)

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
                    self.regions[region].fetch_all(api_client, params['q'], params['targets'])
                except Exception as e:
                    printException(e)
                finally:
                    q.task_done()
        except Exception as e:
            printException(e)
            pass

    def _fetch_target(self, q, params):
        global status
        try:
            while True:
                try:
                    method, region, target = q.get()
                    method(params, region, target)
                    target = method.__name__.replace('parse_', '') + 's'
                    status['counts'][target]['fetched'] += 1
                    if region not in status['regions']:
                        status['regions'].append(region)
                    status_show()
                except Exception as e:
                    printException(e)
                finally:
                    q.task_done()
        except Exception as e:
            printException(e)
            pass



########################################
# RegionConfig
########################################

class RegionConfig(GlobalConfig):
    """
    Base class for ...
    """

    def __init__(self, region_name):
        self.region = region_name

    def fetch_all(self, api_client, q, targets):
        global status
        if targets != None:
            # Ensure targets is a tuple
            if type(targets) != list and type(targets) != tuple:
                targets = tuple(targets,)
            elif type(targets) != tuple:
                targets = tuple(targets)
        else:
            targets = tuple(['%s' % method.replace('fetch_','').title() for method in methods])
        status_init(targets)
        for target in targets:
            target_type = target[0]
            manage_dictionary(status['counts'], target_type, {})
            manage_dictionary(status['counts'][target_type], 'fetched', 0)
            manage_dictionary(status['counts'][target_type], 'discovered', 0)
            self._fetch_targets(api_client, q, target, {})


    def _fetch_targets(self, api_client, q, target, list_params):
        global counts
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
        status['counts'][target_type]['discovered'] += len(targets)
        region = api_client._client_config.region_name
        # Queue resources
        for target in targets:
            callback = getattr(self, 'parse_%s' % target_type[0:-1])
            if q:
                # Add to the queue
                q.put((callback, region, target))
        if not len(targets) and region not in status['regions']:
            status['regions'].append(region)



########################################
# Status updates
########################################

def status_init(targets):
    global formatted_string
    target_names = ()
    if formatted_string == None:
        formatted_string = '\r %18s'
        for t in targets:
            if type(t) == tuple:
                t = t[0]
            target_names += (t,)
            formatted_string += ' %18s'
        status_out(('Regions', ) + target_names, True)

def status_show(newline = False):
    global counts
    #TODO: fix target order mismatch between init and show
    #TODO: fix target not initialized at first prints (when large number of targets)
    targets = ('%d/%d' % (len(status['regions']), status['regions_count']), )
    for t in status['counts']:
        tmp = '%d/%d' % (status['counts'][t]['fetched'], status['counts'][t]['discovered'])
        targets += (tmp,)
    status_out(targets, newline)

def status_out(targets, newline):
    try:
        global formatted_string
        sys.stdout.write(formatted_string % targets)
        sys.stdout.flush()
        if newline:
            sys.stdout.write('\n')
    except:
        pass
