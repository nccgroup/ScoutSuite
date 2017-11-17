# -*- coding: utf-8 -*-
"""
Base classes and functions for region-specific services
"""

import copy
import re

from threading import Event, Thread
# Python2 vs Python3
try:
    from Queue import Queue
except ImportError:
    from queue import Queue

from opinel.utils.aws import build_region_list, connect_service, get_aws_account_id, get_name, handle_truncated_response
from opinel.utils.console import printException, printInfo
from opinel.utils.globals import manage_dictionary

from AWSScout2.configs import resource_id_map
from AWSScout2.configs.threads import thread_configs
from AWSScout2.configs.vpc import VPCConfig
from AWSScout2.utils import format_service_name, is_throttled
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

    def __init__(self, service_metadata = {}, thread_config = 4):
        self.regions = {}
        self.thread_config = thread_configs[thread_config]
        self.service = type(self).__name__.replace('Config', '').lower() # TODO: use regex with EOS instead of plain replace
        if service_metadata != {}:
            self.resource_types = {'global': [], 'region': [], 'vpc': []}
            self.targets = {'first_region': (), 'other_regions': ()}
            for resource in service_metadata['resources']:
                only_first_region = False
                if re.match(r'.*?\.vpcs\.id\..*?', service_metadata['resources'][resource]['path']):
                    self.resource_types['vpc'].append(resource)
                elif re.match(r'.*?\.regions\.id\..*?', service_metadata['resources'][resource]['path']):
                    self.resource_types['region'].append(resource)
                else:
                    only_first_region = True
                    self.resource_types['global'].append(resource)
                resource_metadata = service_metadata['resources'][resource]
                if 'api_call' not in resource_metadata:
                    continue
                params = resource_metadata['params'] if 'params' in resource_metadata else {}
                ignore_exceptions = True if 'no_exceptions' in resource_metadata and resource_metadata['no_exceptions'] == True else False
                if not only_first_region:
                    self.targets['other_regions'] += ((resource, resource_metadata['response'], resource_metadata['api_call'], params, ignore_exceptions),)
                self.targets['first_region'] += ((resource, resource_metadata['response'], resource_metadata['api_call'], params, ignore_exceptions),)


    def init_region_config(self, region):
        """
        Initialize the region's configuration

        :param region:                  Name of the region
        """
        self.regions[region] = self.region_config_class(region_name = region, resource_types = self.resource_types)


    def fetch_all(self, credentials, regions = [], partition_name = 'aws', targets = None):
        """
        Fetch all the configuration supported by Scout2 for a given service

        :param credentials:             F
        :param service:                 Name of the service
        :param regions:                 Name of regions to fetch data from
        :param partition_name:          AWS partition to connect to
        :param targets:                 Type of resources to be fetched; defaults to all.

        """
        # Initialize targets
        # Tweak params
        realtargets = ()
        if not targets:
            targets = self.targets
        for i, target in enumerate(targets['first_region']):
            params = self.tweak_params(target[3], credentials)
            realtargets = realtargets + ((target[0], target[1], target[2], params, target[4]),)
        targets['first_region'] = realtargets
        realtargets = ()
        for i, target in enumerate(targets['other_regions']):
            params = self.tweak_params(target[3], credentials)
            realtargets = realtargets + ((target[0], target[1], target[2], params, target[4]),)
        targets['other_regions'] = realtargets

        printInfo('Fetching %s config...' % format_service_name(self.service))
        self.fetchstatuslogger = FetchStatusLogger(targets['first_region'], True)
        api_service = 'ec2' if self.service.lower() == 'vpc' else self.service.lower()
        # Init regions
        regions = build_region_list(api_service, regions, partition_name) # TODO: move this code within this class
        self.fetchstatuslogger.counts['regions']['discovered'] = len(regions)
        # Threading to fetch & parse resources (queue consumer)
        q = self._init_threading(self._fetch_target, {}, self.thread_config['parse'])
        # Threading to list resources (queue feeder)
        qr = self._init_threading(self._fetch_region, {'api_service': api_service, 'credentials': credentials, 'q': q, 'targets': ()}, self.thread_config['list'])
        # Go
        for i, region in enumerate(regions):
            qr.put((region, targets['first_region'] if i == 0 else targets['other_regions']))
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
                    region, targets = q.get()
                    #print('Targets for region %s : %s' % (region, str(targets)))
                    self.init_region_config(region)
                    api_client = connect_service(params['api_service'], params['credentials'], region, silent = True)
                    api_clients[region] = api_client
                    # TODO : something here for single_region stuff
                    self.regions[region].fetch_all(api_client, self.fetchstatuslogger, params['q'], targets) #  params['targets'])
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
                    backup = copy.deepcopy(target)

                    if method.__name__ == 'store_target':
                        target_type = target['scout2_target_type']
                    else:
                        target_type = method.__name__.replace('parse_', '') + 's'
                    method(params, region, target)
                    self.fetchstatuslogger.counts[target_type]['fetched'] += 1
                    self.fetchstatuslogger.show()
                except Exception as e:
                    if is_throttled(e):
                        q.put((method, region, backup))
                    else:
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


    def tweak_params(self, params, credentials):
        if type(params) == dict:
            for k in params:
                params[k] = self.tweak_params(params[k], credentials)
        elif type(params) == list:
            newparams = []
            for v in params:
                newparams.append(self.tweak_params(v, credentials))
            params = newparams
        else:
            if params == '_AWS_ACCOUNT_ID_':
                params = get_aws_account_id(credentials)
        return params



########################################
# RegionConfig
########################################

class RegionConfig(GlobalConfig):
    """
    Base class for ...
    """

    def __init__(self, region_name, resource_types = {}):
        self.region = region_name
        for resource_type in resource_types['region'] + resource_types['global']:
            setattr(self, resource_type, {})
            setattr(self, '%s_count' % resource_type, 0)
        if len(resource_types['vpc']) > 0:
            setattr(self, 'vpcs', {})
            self.vpc_resource_types = resource_types['vpc']


    def fetch_all(self, api_client, fetchstatuslogger, q, targets):
        self.fetchstatuslogger = fetchstatuslogger
        if targets != None:
            # Ensure targets is a tuple
            if type(targets) != list and type(targets) != tuple:
                targets = tuple(targets,)
            elif type(targets) != tuple:
                targets = tuple(targets)
        for target in targets:
            self._fetch_targets(api_client, q, target)


    def _fetch_targets(self, api_client, q, target):
        # Handle & format the target type
        target_type, response_attribute, list_method_name, list_params, ignore_list_error = target
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
            try:
                callback = getattr(self, 'parse_%s' % target_type[0:-1])
            except:
                callback = self.store_target
                target['scout2_target_type'] = target_type
            if q:
                # Add to the queue
                q.put((callback, region, target))

    def store_target(self, global_params, region, target):
        target_type = target.pop('scout2_target_type')
        if 'VpcId' in target:
            vpc_id = target.pop('VpcId')
            manage_dictionary(self.vpcs, vpc_id, VPCConfig(self.vpc_resource_types))
            tmp = getattr(self, 'vpcs')[vpc_id]
            target_dict = getattr(tmp, target_type)
        else:
            target_dict = getattr(self, target_type)
        target_id = target[resource_id_map[target_type]]
        get_name(target, target, resource_id_map[target_type])
        target_dict[target_id] = target

