# -*- coding: utf-8 -*-

import copy

from hashlib import sha1
from threading import Event, Thread
# Python2 vs Python3
try:
    from Queue import Queue
except ImportError:
    from queue import Queue

from opinel.utils.aws import build_region_list, connect_service, handle_truncated_response
from opinel.utils.console import printException, printInfo

from AWSScout2.configs.threads import thread_configs
from AWSScout2.output.console import FetchStatusLogger
from AWSScout2.utils import format_service_name

########################################
# Globals
########################################

status = None
formatted_string = None


class GlobalConfig(object):

    def get_non_aws_id(self, name):
        """
        Not all AWS resources have an ID and some services allow the use of "." in names, which break's Scout2's
        recursion scheme if name is used as an ID. Use SHA1(name) instead.

        :param name:                    Name of the resource to
        :return:                        SHA1(name)
        """
        m = sha1()
        m.update(name.encode('utf-8'))
        return m.hexdigest()


class BaseConfig(GlobalConfig):
    """
    FooBar
    """
    
    def __init__(self, thread_config = 4):
        self.service = type(self).__name__.replace('Config', '').lower()  # TODO: use regex with EOS instead of plain replace
        self.thread_config = thread_configs[thread_config]


    def fetch_all(self, credentials, regions = [], partition_name = 'aws', targets = None):
        """
        Generic fetching function that iterates through all of the service's targets

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
        formatted_string = None
        api_service = self.service.lower()
        # Connect to the service
        if self.service in [ 's3' ]: # S3 namespace is global but APIs aren't....
            api_clients = {}
            for region in build_region_list(self.service, regions, partition_name):
                api_clients[region] = connect_service('s3', credentials, region, silent = True)
            api_client = api_clients[list(api_clients.keys())[0]]
        elif self.service == 'route53domains':
            api_client = connect_service(self.service, credentials, 'us-east-1', silent = True) # TODO: use partition's default region
        else:
            api_client = connect_service(self.service, credentials, silent = True)
        # Threading to fetch & parse resources (queue consumer)
        params = {'api_client': api_client}
        if self.service in ['s3']:
            params['api_clients'] = api_clients
        q = self._init_threading(self.__fetch_target, params, self.thread_config['parse'])
        # Threading to list resources (queue feeder)
        params = {'api_client': api_client, 'q': q}
        if self.service in ['s3']:
            params['api_clients'] = api_clients
        qt = self._init_threading(self.__fetch_service, params, self.thread_config['list'])
        # Init display
        self.fetchstatuslogger = FetchStatusLogger(targets)
        # Go
        for target in targets:
            qt.put(target)
        # Join
        qt.join()
        q.join()
        # Show completion and force newline
        if self.service != 'iam':
            self.fetchstatuslogger.show(True)


    def finalize(self):
        for t in self.fetchstatuslogger.counts:
            setattr(self, '%s_count' % t, self.fetchstatuslogger.counts[t]['fetched'])
        self.__delattr__('fetchstatuslogger')


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


    def __fetch_service(self, q, params):
        api_client = params['api_client']
        try:
            while True:
                try:
                    target_type, response_attribute, list_method_name, list_params, ignore_list_error = q.get()
                    if not list_method_name:
                        continue
                    try:
                        method = getattr(api_client, list_method_name)
                    except Exception as e:
                        printException(e)
                        continue
                    try:
                        if type(list_params) != list:
                            list_params = [ list_params ]
                        targets = []
                        for lp in list_params:
                            targets += handle_truncated_response(method, lp, [response_attribute])[response_attribute]
                    except Exception as e:
                        if not ignore_list_error:
                            printException(e)
                        targets = []
                    self.fetchstatuslogger.counts[target_type]['discovered'] += len(targets)
                    for target in targets:
                        params['q'].put((target_type, target),)
                except Exception as e:
                    printException(e)
                finally:
                    q.task_done()
        except Exception as e:
            printException(e)
            pass


    def __fetch_target(self, q, params):
        global status
        try:
            while True:
                try:
                    target_type, target = q.get()
                    # Make a full copy of the target in case we need to re-queue it
                    backup = copy.deepcopy(target)
                    method = getattr(self, 'parse_%s' % target_type)
                    method(target, params)
                    self.fetchstatuslogger.counts[target_type]['fetched'] += 1
                    self.fetchstatuslogger.show()
                except Exception as e:
                    if hasattr(e, 'response') and 'Error' in e.response and e.response['Error']['Code'] in [ 'Throttling' ]:
                        q.put((target_type, backup),)
                    else:
                        printException(e)
                finally:
                    q.task_done()
        except Exception as e:
            printException(e)
            pass
