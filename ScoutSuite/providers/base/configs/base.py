# -*- coding: utf-8 -*-

import copy

from threading import Thread

# Python2 vs Python3
try:
    from Queue import Queue
except ImportError:
    from queue import Queue

from hashlib import sha1

from ScoutSuite.providers.base.configs.threads import thread_configs

# TODO do this better without name conflict
from opinel.utils.aws import connect_service
from ScoutSuite.providers.gcp.utils import gcp_connect_service
from ScoutSuite.providers.azure.utils import azure_connect_service

from opinel.utils.aws import build_region_list
from opinel.utils.console import printException, printInfo

from ScoutSuite.output.console import FetchStatusLogger
from ScoutSuite.utils import format_service_name

# TODO global is trash
status = None
formatted_string = None


class BaseConfig(object):

    def __init__(self, thread_config=4, **kwargs):
        """

        :param thread_config:
        """

        self.library_type = None if not hasattr(self, 'library_type') else self.library_type

        self.service = type(self).__name__.replace('Config',
                                                   '').lower()  # TODO: use regex with EOS instead of plain replace
        self.thread_config = thread_configs[thread_config]

        # Booleans that define if threads should keep running
        self.run_service_threads = True
        self.run_target_threads = True

    def _is_provider(self, provider_name):
        return False

    def get_non_provider_id(self, name):
        """
        Not all AWS resources have an ID and some services allow the use of "." in names, which break's Scout2's
        recursion scheme if name is used as an ID. Use SHA1(name) instead.

        :param name:                    Name of the resource to
        :return:                        SHA1(name)
        """
        m = sha1()
        m.update(name.encode('utf-8'))
        return m.hexdigest()

    def fetch_all(self, credentials, regions=None, partition_name='aws', targets=None):
        """
        :param credentials:             F
        :param service:                 Name of the service
        :param regions:                 Name of regions to fetch data from
        :param partition_name:          AWS partition to connect to
        :param targets:                 Type of resources to be fetched; defaults to all.
        :return:
        """
        regions = [] if regions is None else regions
        global status, formatted_string

        # Initialize targets
        if not targets:
            targets = type(self).targets
        printInfo('Fetching %s config...' % format_service_name(self.service))
        formatted_string = None

        # FIXME the below should be in moved to each provider's code

        # Connect to the service
        if self._is_provider('aws'):
            if self.service in ['s3']:  # S3 namespace is global but APIs aren't....
                api_clients = {}
                for region in build_region_list(self.service, regions, partition_name):
                    api_clients[region] = connect_service('s3', credentials, region, silent=True)
                api_client = api_clients[list(api_clients.keys())[0]]
            elif self.service == 'route53domains':
                api_client = connect_service(self.service, credentials, 'us-east-1',
                                             silent=True)  # TODO: use partition's default region
            else:
                api_client = connect_service(self.service, credentials, silent=True)

        elif self._is_provider('gcp'):
            api_client = gcp_connect_service(service=self.service, credentials=credentials)

        elif self._is_provider('azure'):
            api_client = azure_connect_service(service=self.service, credentials=credentials)

        # Threading to fetch & parse resources (queue consumer)
        params = {'api_client': api_client}

        if self._is_provider('aws'):
            if self.service in ['s3']:
                params['api_clients'] = api_clients

        # Threading to parse resources (queue feeder)
        target_queue = self._init_threading(self.__fetch_target, params, self.thread_config['parse'])

        # Threading to list resources (queue feeder)
        params = {'api_client': api_client, 'q': target_queue}

        if self._is_provider('aws'):
            if self.service in ['s3']:
                params['api_clients'] = api_clients

        service_queue = self._init_threading(self.__fetch_service, params, self.thread_config['list'])

        # Init display
        self.fetchstatuslogger = FetchStatusLogger(targets)

        # Go
        for target in targets:
            service_queue.put(target)

        # Blocks until all items in the queue have been gotten and processed.
        service_queue.join()
        target_queue.join()

        # Show completion and force newline
        if self._is_provider('aws'):
            # Show completion and force newline
            if self.service != 'iam':
                self.fetchstatuslogger.show(True)
        else:
            self.fetchstatuslogger.show(True)

        # Threads should stop running as queues are empty
        self.run_target_threads = False
        self.run_service_threads = False
        # Put x items in the queues to ensure threads run one last time (and exit)
        for i in range(self.thread_config['parse']):
            target_queue.put(None)
        for j in range(self.thread_config['list']):
            service_queue.put(None)

    def __fetch_target(self, q, params):
        global status
        try:
            while self.run_target_threads:
                try:
                    target_type, target = q.get() or (None, None)
                    if target_type and target:
                        # Make a full copy of the target in case we need to re-queue it
                        backup = copy.deepcopy(target)
                        method = getattr(self, 'parse_%s' %
                                         target_type.replace('.', '_'))  # TODO fix this, hack for GCP API Client libs
                        method(target, params)
                        self.fetchstatuslogger.counts[target_type]['fetched'] += 1
                        self.fetchstatuslogger.show()
                except Exception as e:
                    if hasattr(e, 'response') and \
                            'Error' in e.response and \
                            e.response['Error']['Code'] in ['Throttling']:
                        q.put((target_type, backup), )
                    else:
                        printException(e)
                finally:
                    q.task_done()
        except Exception as e:
            printException(e)
            pass

    def __fetch_service(self, q, params):
        api_client = params['api_client']
        try:
            while self.run_service_threads:
                try:
                    target_type, response_attribute, list_method_name, list_params, ignore_list_error = q.get() or (None, None, None, None, None)

                    if target_type:

                        if not list_method_name:
                            continue

                        try:
                            method = self._get_method(api_client, target_type, list_method_name)
                        except Exception as e:
                            printException(e)
                            continue

                        try:
                            targets = self._get_targets(response_attribute, api_client, method, list_params, ignore_list_error)
                        except Exception as e:
                            if not ignore_list_error:
                                printException(e)
                            targets = []

                        self.fetchstatuslogger.counts[target_type]['discovered'] += len(targets)

                        for target in targets:
                            params['q'].put((target_type, target), )

                except Exception as e:
                    printException(e)
                finally:
                    q.task_done()
        except Exception as e:
            printException(e)
            pass

    def _get_method(self, api_client, target_type, list_method_name):
        """
        Gets the appropriate method, required as each provider may have particularities

        :return:
        """
        return None

    def _get_targets(self, response_attribute, api_client, method, list_params, ignore_list_error):
        """
        Gets the targets, required as each provider may have particularities

        :return:
        """
        return None

    def finalize(self):
        for t in self.fetchstatuslogger.counts:
            setattr(self, '%s_count' % t, self.fetchstatuslogger.counts[t]['fetched'])
        self.__delattr__('fetchstatuslogger')

    def _init_threading(self, function, params=None, num_threads=10):
        params = {} if params is None else params
        # Init queue and threads
        q = Queue(maxsize=0)  # TODO: find something appropriate
        for i in range(num_threads):
            worker = Thread(target=function, args=(q, params))
            worker.setDaemon(True)
            worker.start()
        return q
