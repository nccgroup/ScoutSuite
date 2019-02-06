# -*- coding: utf-8 -*-

# Python2 vs Python3
try:
    from Queue import Queue
except ImportError:
    from queue import Queue

import itertools
import json
import re

from google.api_core.exceptions import PermissionDenied
from google.cloud import container_v1
from googleapiclient.errors import HttpError

from opinel.utils.console import printException, printError

from ScoutSuite.providers.base.configs.base import BaseConfig
from ScoutSuite.providers.gcp.utils import gcp_connect_service

class GCPBaseConfig(BaseConfig):

    def __init__(self, thread_config=4, projects=None, **kwargs):
        projects = [] if projects is None else projects

        self.projects = projects

        self.error_list = []  # list of errors, so that we don't print the same error multiple times

        self.zones = None
        self.regions = None

        super(GCPBaseConfig, self).__init__(thread_config)

    def _is_provider(self, provider_name):
        return provider_name == 'gcp'

    def get_regions(self, **kwargs):
        """
        Certain services require to be poled per-region.
        In these cases, this method will return a list of regions to poll.

        :return:
        """

        computeengine_client = gcp_connect_service(service='computeengine')

        if not self.regions:
            # get regions from a project that has CE API enabled
            for project in self.projects:
                try:
                    regions_list = []
                    regions = computeengine_client.regions().list(project=project['projectId']).execute()['items']
                    for region in regions:
                        regions_list.append(region['name'])
                    self.regions = regions_list
                except HttpError as e:
                    pass
                except Exception as e:
                    printException(e)
                if self.regions:
                    break

        return self.regions

    def get_zones(self, **kwargs):
        """
        Certain services require to be poled per-zone.
        In these cases, this method will return a list of zones to poll.

        :return:
        """

        computeengine_client = gcp_connect_service(service='computeengine')

        if not self.zones:
            # get zones from a project that has CE API enabled
            for project in self.projects:
                try:
                    zones_list = []
                    zones = computeengine_client.zones().list(project=project['projectId']).execute()['items']
                    for zone in zones:
                        zones_list.append(zone['name'])
                    self.zones = zones_list
                except HttpError as e:
                    pass
                except Exception as e:
                    printException(e)
                if self.zones:
                    break

        return self.zones

    def _get_method(self, api_client, target_type, list_method_name):
        """
        Gets the appropriate method, required as each provider may have particularities

        :return:
        """

        # This is a specific case for GCP services that don't have a native cloud library
        if self.library_type == 'api_client_library':
            # Required for nested targers, e.g. projects().resource().list()
            target = getattr(api_client, target_type.split('.')[0])
            for t in target_type.split('.')[1:]:
                target = getattr(target(), t)
                # target_type = type  # hack to display the last element
            method = getattr(target(), list_method_name)
        # This works for AWS and GCP cloud libraries
        else:
            method = getattr(api_client, list_method_name)

        return method

    def _get_targets(self, response_attribute, api_client, method, list_params, ignore_list_error):
        """
        Fetch the targets, required as each provider may have particularities

        :return:
        """

        targets = []

        try:

            regions = self.get_regions()
            zones = self.get_zones()

            # Create a list with all combinations for method parameters
            list_params_list = []

            # Dict for all the elements to combine
            combination_elements = {'project_placeholder': [project['projectId'] for project in self.projects],
                                    'region_placeholder': regions,
                                    'zone_placeholder': zones}

            # Get a list of {{}} terms
            sources = re.findall("{{(.*?)}}", str(list_params.values()))
            # Remove keys from combinations if they aren't in the sources
            confirmed_combination_elements = {}
            for source in sources:
                confirmed_combination_elements[source] = combination_elements[source]
            # Build a list of the possible combinations
            combinations = self._dict_product(confirmed_combination_elements)
            for combination in combinations:
                l = list_params.copy()
                for k, v in l.items():
                    k1 = re.findall("{{(.*?)}}", v)
                    if k1:
                        l[k] = l[k].replace('{{%s}}' % k1[0], combination[k1[0]])
                list_params_list.append(l)

            for list_params_combination in list_params_list:

                try:

                    if self.library_type == 'cloud_client_library':

                        # TODO this should be more modular
                        # this is only for stackdriverlogging
                        if self.service == 'stackdriverlogging':
                            api_client.project = list_params_combination.pop('project')

                        response = method(**list_params_combination)

                        # TODO this should be more modular
                        # this is only for kubernetesengine
                        if isinstance(response, container_v1.types.ListClustersResponse):
                            targets += response.clusters
                        else:
                            targets += list(response)

                        # Remove client as it's unpickleable and adding the object to the Queue will pickle
                        # The client is later re-inserted in each Config
                        for t in targets:
                            if hasattr(t, '_client'):
                                t._client = None

                    if self.library_type == 'api_client_library':

                        # TODO need to handle long responses
                        request = method(**list_params_combination)
                        while request is not None:
                            response = request.execute()

                            if 'items' in response:
                                targets += response['items']
                            # TODO this should be more modular
                            # this is only for cloudresourcemanager
                            if 'bindings' in response:
                                targets += response['bindings']
                            # TODO this should be more modular
                            # this is only for IAM
                            if 'accounts' in response:
                                targets += response['accounts']

                            # TODO need to define the _next to handle long responses
                            # request = method_next(previous_request=request,
                            #                       previous_response=response)
                            request = None

                except HttpError as e:
                    error_json = json.loads(e.content)
                    if error_json['error']['message'] not in self.error_list:
                        self.error_list.append(error_json['error']['message'])
                        printError(error_json['error']['message'])

                except PermissionDenied as e:
                    printError("%s: %s - %s" % (e.message, self.service, self.targets))

                except Exception as e:
                    printException(e)

        except HttpError as e:
            error_json = json.loads(e.content)
            if error_json['error']['message'] not in self.error_list:
                self.error_list.append(error_json['error']['message'])
                printError(error_json['error']['message'])

        except Exception as e:
            printException(e)

        finally:
            return targets

    def _dict_product(self, d):
        keys = d.keys()
        for element in itertools.product(*d.values()):
            yield dict(zip(keys, element))
