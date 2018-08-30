# -*- coding: utf-8 -*-

import copy

from hashlib import sha1
from threading import Thread

# Python2 vs Python3
try:
    from Queue import Queue
except ImportError:
    from queue import Queue

from google.cloud import storage

from opinel.utils.aws import build_region_list, handle_truncated_response
from opinel.utils.console import printException, printInfo

from ScoutSuite.providers.gcp.utils import connect_service
from ScoutSuite.providers.base.configs.threads import thread_configs
from ScoutSuite.output.console import FetchStatusLogger
from ScoutSuite.utils import format_service_name
from ScoutSuite.providers.base.configs.base import GlobalConfig

status = None
formatted_string = None

class GCPBaseConfig(GlobalConfig):

    def fetch_all(self, credentials, regions=[], partition_name='gcp', targets=None):
        """
        :param credentials:             F
        :param service:                 Name of the service
        :param regions:                 Name of regions to fetch data from
        :param partition_name:          AWS partition to connect to
        :param targets:                 Type of resources to be fetched; defaults to all.
        :return:
        """
        global status, formatted_string

        # Initialize targets
        if not targets:
            targets = type(self).targets
        printInfo('Fetching %s config...' % format_service_name(self.service))
        formatted_string = None

        # Connect to the service
        api_client = connect_service(service=self.service, credentials=credentials)

        # Threading to fetch & parse resources (queue consumer)
        params = {'api_client': api_client}

        # Threading to parse resources (queue feeder)
        target_queue = self._init_threading(self.__fetch_target, params, self.thread_config['parse'])

        # Threading to list resources (queue feeder)
        params = {'api_client': api_client, 'q': target_queue}

        service_queue = self._init_threading(self.__fetch_service, params, self.thread_config['list'])

        # Init display
        self.fetchstatuslogger = FetchStatusLogger(targets)

        # Go
        for target in targets:
            service_queue.put(target)

        # Join
        service_queue.join()
        target_queue.join()


    def finalize(self):
        for t in self.fetchstatuslogger.counts:
            setattr(self, '%s_count' % t, self.fetchstatuslogger.counts[t]['fetched'])
        self.__delattr__('fetchstatuslogger')

    def _init_threading(self, function, params={}, num_threads=10):
        # Init queue and threads
        q = Queue(maxsize=0)  # TODO: find something appropriate
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
                        response = method(**list_params)
                        targets = list(response)
                        # Remove client as it's unpickleable and adding the Bucket object to the Queue will pickle
                        # The client is re-inserted in each config
                        for bucket in targets:
                            bucket._client = None
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

    def __fetch_target(self, q, params):
        # TODO this is copied from AWS's AWSBaseConfig
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
