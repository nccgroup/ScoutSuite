# -*- coding: utf-8 -*-

from hashlib import sha1
import sys
from threading import Event, Thread
# Python2 vs Python3
try:
    from Queue import Queue
except ImportError:
    from queue import Queue

from opinel.utils import build_region_list, connect_service, handle_truncated_response, manage_dictionary, printException, printInfo

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
    
    def __init__(self):
        self.service = type(self).__name__.replace('Config', '').lower()  # TODO: use regex with EOS instead of plain replace
        self.counts = {}


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
        formatted_string = None
        #self.status_init(targets)
        api_service = self.service.lower() # TODO : handle EC2/VPC/ELB weirdness maybe ?
        # Connect to the service
        if self.service in [ 's3' ]: # grmbl
            api_clients = {}
            for region in build_region_list(self.service, regions, partition_name):
                api_clients[region] = connect_service('s3', credentials, region)
            api_client = api_clients[api_clients.keys()[0]]
        else:
            api_client = connect_service(self.service, credentials)
        # Threading to fetch & parse resources (queue consumer)
        params = {'api_client': api_client}
        if self.service in ['s3']:
            params['api_clients'] = api_clients
        q = self._init_threading(self.__fetch_target, params, 20)
        # Threading to list resources (queue feeder)
        params = {'api_client': api_client, 'q': q}
        if self.service in ['s3']:
            params['api_clients'] = api_clients
        qt = self._init_threading(self.__fetch_service, params, 10)
        # Go
        for target in targets:
            target_type = target[0]
            manage_dictionary(self.counts, target_type, {})
            manage_dictionary(self.counts[target_type], 'fetched', 0)
            manage_dictionary(self.counts[target_type], 'discovered', 0)
            qt.put(target)
        self.status_init() # targets)
        # Join
        qt.join()
        q.join()
        # Show completion and force newline
        self.status_show(True)
        # Remove temporary counters and update service config
        try:
            for t in self.counts:
                count = '%s_count' % t
                setattr(self, count, self.counts[t]['fetched'])
            self.__delattr__(counts)
        except:
            pass


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
        #printInfo(str(params))
        try:
            while True:
                try:
                    target_type, response_attribute, list_method_name, list_params, ignore_list_error = q.get()
                    try:
                        method = getattr(api_client, list_method_name)
                    except:
                        continue
                    try:
                        targets = handle_truncated_response(method, list_params, [response_attribute])[
                            response_attribute]
                    except Exception as e:
                        if not ignore_list_error:
                            printException(e)
                        targets = []
                    self.counts[target_type]['discovered'] += len(targets)
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
                    method = getattr(self, 'parse_%s' % target_type)
                    method(target, params)
                    self.counts[target_type]['fetched'] += 1
                    self.status_show()
                except Exception as e:
                    printException(e)
                finally:
                    q.task_done()
        except Exception as e:
            printException(e)
            pass





    ########################################
    # Status updates
    ########################################
    
    def status_init(self): # , targets):
        global formatted_string
        target_names = ()
        if formatted_string == None:
            formatted_string = '\r'
            for t in self.counts:
                target_names += (t,)
                formatted_string += ' %18s'
            self.status_out(target_names, True)
    
    def status_show(self, newline = False):
        targets = ()
        for t in self.counts:
            tmp = '%d/%d' % (self.counts[t]['fetched'], self.counts[t]['discovered'])
            targets += (tmp,)
        self.status_out(targets, newline)
    
    def status_out(selft, targets, newline):
        try:
            global formatted_string
            sys.stdout.write(formatted_string % targets)
            sys.stdout.flush()
            if newline:
                sys.stdout.write('\n')
        except:
            pass