# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import unicode_literals

import json
import sys
import copy

from opinel.utils.console import printException, printInfo
from opinel.utils.globals import manage_dictionary

from ScoutSuite import __version__ as scout2_version
from ScoutSuite.providers.base.configs.browser import get_object_at
from ScoutSuite.output.html import Scout2Report


class BaseProvider(object):
    """
    Base class for the different providers.

    Root object that holds all of the necessary provider-specific resources and Scout configuration items.

    For each supported cloud provider, a child class will be created which implements the necessary code.
    In addition, each method of children classes will call the base provider in order to execute code required for
    all cloud providers
    """

    def __init__(self, report_dir=None, timestamp=None, services=None, skipped_services=None, thread_config=4, **kwargs):
        """

        :aws_account_id     AWS account ID
        :last_run           Information about the last run
        :metadata           Metadata used to generate the HTML report
        :ruleset            Ruleset used to perform the analysis
        :services           AWS configuration sorted by service
        """
        services = [] if services is None else services
        skipped_services = [] if skipped_services is None else skipped_services

        self.credentials = None
        self.last_run = None
        self.metadata = None

        self._load_metadata()

        self.services = self.services_config(self.metadata, thread_config)
        supported_services = vars(self.services).keys()
        self.service_list = self._build_services_list(supported_services, services, skipped_services)

    def authenticate(self):
        """
        Authenticate to the provider using provided credentials
        :return:
        """
        pass

    def preprocessing(self, ip_ranges=None, ip_ranges_name_key=None):
        """
        TODO

        :return: None
        """
        ip_ranges = [] if ip_ranges is None else ip_ranges

        # Preprocessing dictated by metadata
        self._process_metadata_callbacks()

    def postprocessing(self, current_time, ruleset):
        """
        TODO

        :param config:
        :param current_time:
        :param ruleset:
        :return: None
        """
        self._update_metadata()
        self._update_last_run(current_time, ruleset)

    def fetch(self, regions=None, skipped_regions=None, partition_name=None):
        """
        Fetch resources for each service

        :param services:
        :param skipped_services:
        :param regions:
        :param skipped_regions:
        :param partition_name:
        :return:
        """
        regions = [] if regions is None else regions
        skipped_regions = [] if skipped_regions is None else skipped_regions
        # TODO: determine partition name based on regions and warn if multiple partitions...
        self.services.fetch(self.credentials, self.service_list, regions)

        # TODO implement this properly
        """
        This is quite ugly but the legacy Scout2 expects the configurations to be dictionaries.
        Eventually this should be moved to objects/attributes, but that will require significan re-write.
        """
        report = Scout2Report(self.provider_code,
                              self.profile)
        self.services = report.jsrw.to_dict(self.services)

    def _load_metadata(self):
        """
        Load the metadata as defined in the child class metadata_path attribute

        :return: None
        """
        # Load metadata
        with open(self.metadata_path, 'rt') as f:
            self.metadata = json.load(f)

    def _build_services_list(self, supported_services, services, skipped_services):
        return [s for s in supported_services if (services == [] or s in services) and s not in skipped_services]

    def _update_last_run(self, current_time, ruleset):
        last_run = {}
        last_run['time'] = current_time.strftime("%Y-%m-%d %H:%M:%S%z")
        last_run['cmd'] = ' '.join(sys.argv)
        last_run['version'] = scout2_version
        last_run['ruleset_name'] = ruleset.name
        last_run['ruleset_about'] = ruleset.about
        last_run['summary'] = {}
        for service in self.services:
            last_run['summary'][service] = {'checked_items': 0, 'flagged_items': 0, 'max_level': 'warning',
                                            'rules_count': 0, 'resources_count': 0}
            if self.services[service] == None:
                # Not supported yet
                continue
            elif 'findings' in self.services[service]:
                for finding in self.services[service]['findings'].values():
                    last_run['summary'][service]['rules_count'] += 1
                    last_run['summary'][service]['checked_items'] += finding['checked_items']
                    last_run['summary'][service]['flagged_items'] += finding['flagged_items']
                    items = finding.get('items', [])
                    if last_run['summary'][service]['max_level'] != 'danger' and len(items) > 0:
                        last_run['summary'][service]['max_level'] = finding['level']
            # Total number of resources
            for key in self.services[service]:
                if key != 'regions_count' and key.endswith('_count'):
                    last_run['summary'][service]['resources_count'] += self.services[service][key]
        self.last_run = last_run

    def _update_metadata(self):
        service_map = {}
        for service_group in self.metadata:
            for service in self.metadata[service_group]:
                if service not in self.service_list:
                    continue
                if 'hidden' in self.metadata[service_group][service] and \
                        self.metadata[service_group][service]['hidden'] == True:
                    continue
                if 'resources' not in self.metadata[service_group][service]:
                    continue
                service_map[service] = service_group
                for resource in self.metadata[service_group][service]['resources']:
                    # full_path = path if needed
                    if not 'full_path' in self.metadata[service_group][service]['resources'][resource]:
                        self.metadata[service_group][service]['resources'][resource]['full_path'] = \
                            self.metadata[service_group][service]['resources'][resource]['path']
                    # Script is the full path minus "id" (TODO: change that)
                    if not 'script' in self.metadata[service_group][service]['resources'][resource]:
                        self.metadata[service_group][service]['resources'][resource]['script'] = '.'.join(
                            [x for x in
                             self.metadata[service_group][service]['resources'][resource]['full_path'].split(
                                 '.') if x != 'id'])
                    
                    # Update counts
                    service_config = self.services[service]
                    if not service_config :
                        continue
                    
                    count = '%s_count' % resource
                    if resource != 'regions':
                        if 'regions' in service_config.keys() and isinstance(service_config['regions'], dict):
                            self.metadata[service_group][service]['resources'][resource]['count'] = 0
                            for region in service_config['regions']:
                                if count in service_config['regions'][region].keys():
                                    self.metadata[service_group][service]['resources'][resource]['count'] += \
                                        service_config['regions'][region][count]
                        else:
                            try:
                                self.metadata[service_group][service]['resources'][resource]['count'] = \
                                    service_config[count]
                            except Exception as e:
                                printException(e)
                    else:
                        self.metadata[service_group][service]['resources'][resource]['count'] = len(service_config['regions'])


    def manage_object(self, object, attr, init, callback=None):
        """
        This is a quick-fix copy of Opine's manage_dictionary in order to support the new ScoutSuite object which isn't
        a dict
        """
        if type(object) == dict:
            if not str(attr) in object:
                object[str(attr)] = init
                self.manage_object(object, attr, init)
        else:
            if not hasattr(object, attr):
                setattr(object, attr, init)
                self.manage_object(object, attr, init)
        if callback:
            callback(getattr(object, attr))
        return object

    def _process_metadata_callbacks(self):
        """
        Iterates through each type of resource and, when callbacks have been
        configured in the config metadata, recurse through each resource and calls
        each callback.

        :param self.config:                  The entire AWS configuration object
        :return:                            None
        """
        # Service-level summaries
        for service_group in self.metadata:
            for service in self.metadata[service_group]:
                if service == 'summaries':
                    continue
                # Reset external attack surface
                if 'summaries' in self.metadata[service_group][service]:
                    for summary in self.metadata[service_group][service]['summaries']:
                        if summary == 'external attack surface' and \
                                service in self.services and \
                                'external_attack_surface' in self.services[service]:
                            self.services[service].pop('external_attack_surface')
                # Reset all global summaries
                if hasattr(self, 'service_groups'):
                    del self.service_groups
                # Resources
                for resource_type in self.metadata[service_group][service]['resources']:
                    if 'callbacks' in self.metadata[service_group][service]['resources'][resource_type]:
                        current_path = ['services', service]
                        target_path = self.metadata[service_group][service]['resources'][resource_type][
                                          'path'].replace('.id', '').split('.')[2:]
                        callbacks = self.metadata[service_group][service]['resources'][resource_type][
                            'callbacks']
                        self._new_go_to_and_do(self.services[service],
                                               target_path,
                                               current_path,
                                               callbacks)
                # Summaries
                if 'summaries' in self.metadata[service_group][service]:
                    for summary in self.metadata[service_group][service]['summaries']:
                        if 'callbacks' in self.metadata[service_group][service]['summaries'][summary]:
                            current_path = ['services', service]
                            for callback in self.metadata[service_group][service]['summaries'][summary][
                                'callbacks']:
                                callback_name = callback[0]
                                callback_args = copy.deepcopy(callback[1])
                                target_path = callback_args.pop('path').replace('.id', '').split('.')[2:]
                                callbacks = [[callback_name, callback_args]]
                                self._new_go_to_and_do(self.services[service],
                                                       target_path,
                                                       current_path,
                                                       callbacks)
        # Group-level summaries
        for service_group in self.metadata:
            if 'summaries' in self.metadata[service_group]:
                for summary in self.metadata[service_group]['summaries']:
                    current_path = ['services', service]
                    for callback in self.metadata[service_group]['summaries'][summary]['callbacks']:
                        callback_name = callback[0]
                        callback_args = copy.deepcopy(callback[1])
                        target_path = self.metadata[service_group]['summaries'][summary]['path'].split('.')
                        # quick fix as legacy Scout2 expects "self" to be a dict
                        target_object = self
                        for p in target_path:
                            self.manage_object(target_object, p, {})
                            if type(target_object) == dict:
                                target_object = target_object[p]
                            else:
                                target_object = getattr(target_object, p)
                        if callback_name == 'merge':
                            for service in self.metadata[service_group]:
                                if service == 'summaries':
                                    continue
                                if 'summaries' in self.metadata[service_group][service] and \
                                        summary in self.metadata[service_group][service]['summaries']:
                                    try:
                                        source = get_object_at(self,
                                                               self.metadata[service_group][service]['summaries'][summary]['path'].split('.'))
                                    except Exception as e:
                                        source = {}
                                    target_object.update(source)

        return None

    def _go_to_and_do(self, current_config, path, current_path, callback, callback_args=None):
        """
        Recursively go to a target and execute a callback
        """
        try:

            key = path.pop(0)
            if not current_config:
                current_config = self.config
            if not current_path:
                current_path = []
            keys = key.split('.')
            if len(keys) > 1:
                while True:
                    key = keys.pop(0)
                    if not len(keys):
                        break
                    current_path.append(key)
                    current_config = current_config[key]
            # if hasattr(current_config, key):
            if key in current_config:
                current_path.append(key)
                # current_config_key = getattr(current_config, key)
                current_config_key = current_config[key]
                for (i, value) in enumerate(list(current_config_key)):
                    if len(path) == 0:
                        if type(current_config_key == dict) and type(value) != dict and type(value) != list:
                            callback(current_config_key[value], path, current_path, value, callback_args)
                        else:
                            callback(current_config, path, current_path, value, callback_args)
                    else:
                        tmp = copy.deepcopy(current_path)
                        try:
                            tmp.append(value)
                            self._go_to_and_do(current_config_key[value], copy.deepcopy(path), tmp, callback,
                                               callback_args)
                        except:
                            tmp.pop()
                            tmp.append(i)
                            self._go_to_and_do(current_config_key[i], copy.deepcopy(path), tmp, callback,
                                               callback_args)

        except Exception as e:
            printException(e)
            printInfo('Path: %s' % str(current_path))
            printInfo('Key = %s' % str(key) if 'key' in locals() else 'not defined')
            printInfo('Value = %s' % str(value) if 'value' in locals() else 'not defined')
            printInfo('Path = %s' % path)

    def _new_go_to_and_do(self, current_config, path, current_path, callbacks):
        """
        Recursively go to a target and execute a callback
        """
        try:

            key = path.pop(0)
            if not current_config:
                current_config = self.config
            if not current_path:
                current_path = []
            keys = key.split('.')
            if len(keys) > 1:
                while True:
                    key = keys.pop(0)
                    if not len(keys):
                        break
                    current_path.append(key)
                    current_config = current_config[key]
            if key in current_config:
                current_path.append(key)
                for (i, value) in enumerate(list(current_config[key])):
                    if len(path) == 0:
                        for callback_info in callbacks:
                            callback_name = callback_info[0]

                            # callback = globals()[callback_name]
                            callback = getattr(self, callback_name)

                            callback_args = callback_info[1]
                            if type(current_config[key] == dict) and type(value) != dict and type(value) != list:
                                callback(current_config[key][value],
                                         path,
                                         current_path,
                                         value,
                                         callback_args)
                            else:
                                callback(current_config, path, current_path, value, callback_args)
                    else:
                        tmp = copy.deepcopy(current_path)
                        try:
                            tmp.append(value)
                            self._new_go_to_and_do(current_config[key][value], copy.deepcopy(path), tmp,
                                                   callbacks)
                        except:
                            tmp.pop()
                            tmp.append(i)
                            self._new_go_to_and_do(current_config[key][i], copy.deepcopy(path), tmp, callbacks)
        except Exception as e:
            printException(e)
            printInfo('Path: %s' % str(current_path))
            printInfo('Key = %s' % str(key) if 'key' in locals() else 'not defined')
            printInfo('Value = %s' % str(value) if 'value' in locals() else 'not defined')
            printInfo('Path = %s' % path)
