# -*- coding: utf-8 -*-

# Python2 vs Python3
try:
    from Queue import Queue
except ImportError:
    from queue import Queue

import json

from googleapiclient.errors import HttpError
from google.api_core.exceptions import PermissionDenied

from opinel.utils.console import printException, printError

from ScoutSuite.providers.base.configs.base import BaseConfig


class GCPBaseConfig(BaseConfig):

    def __init__(self, thread_config=4, projects=[], **kwargs):

        self.projects = projects

        super(GCPBaseConfig, self).__init__(thread_config)

    def _is_provider(self, provider_name):
        if provider_name == 'gcp':
            return True
        else:
            return False

    def get_zones(self, **kwargs):
        """
        Certain services require to be poled per-zone. In these cases, this method will return a list of zones to poll
        or None.

        :return:
        """
        return None

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
        error_list = [] # list of errors, so that we don't print the same error multiple times

        try:

            # FIXME this is temporary, will have to be moved to Config children objects
            # get zones from a project that has CE API enabled
            zones = None
            for project in self.projects:
                try:
                    zones = self.get_zones(client=api_client, project=project['projectId'])
                except HttpError as e:
                    pass
                except Exception as e:
                    printException(e)
                if zones:
                    break
            # What this does is create a list with all combinations of possibilities for method parameters
            list_params_list = []
            # only projects
            if ('project_placeholder' in list_params.values() or 'projects/project_placeholder' in list_params.values())\
                    and not 'zone_placeholder' in list_params.values():
                for project in self.projects:
                    list_params_list.append({key:
                                                 project['projectId'] if list_params[key] == 'project_placeholder'
                                                 else ('projects/%s' % project['projectId'] if list_params[key] == 'projects/project_placeholder'
                                                       else list_params[key])
                                             for key in list_params})
            # only zones
            elif not ('project_placeholder' in list_params.values() or 'projects/project_placeholder' in list_params.values())\
                    and 'zone_placeholder' in list_params.values():
                for zone in zones:
                    list_params_list.append({key:
                                                 zone if list_params[key] == 'zone_placeholder'
                                                 else list_params[key]
                                             for key in list_params})
            # projects and zones
            elif ('project_placeholder' in list_params.values() or 'projects/project_placeholder' in list_params.values())\
                    and 'zone_placeholder' in list_params.values():
                import itertools
                for elem in list(itertools.product(*[self.projects, zones])):
                    list_params_list.append({key:
                                                 elem[0]['projectId'] if list_params[key] == 'project_placeholder'
                                                 else ('projects/%s' % elem[0]['projectId'] if list_params[key] == 'projects/project_placeholder'
                                                       else (elem[1] if list_params[key] == 'zone_placeholder'
                                                             else list_params[key]))
                                             for key in list_params})
            # neither projects nor zones
            else:
                list_params_list.append(list_params)

            for list_params_combination in list_params_list:

                try:

                    if self.library_type == 'cloud_client_library':
                        response = method(**list_params_combination)
                        targets += list(response)
                        # Remove client as it's unpickleable and adding the object to the Queue will pickle
                        # The client is later re-inserted in each Config
                        for t in targets:
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
                            # this is only for IAM
                            if 'accounts' in response:
                                targets += response['accounts']

                            # TODO need to define the _next to handle long responses
                            # request = method_next(previous_request=request,
                            #                       previous_response=response)
                            request = None

                except HttpError as e:
                    error_json = json.loads(e.content)
                    if error_json['error']['message'] not in error_list:
                        error_list.append(error_json['error']['message'])
                        printError(error_json['error']['message'])

                except PermissionDenied as e:
                    printError("%s: %s - %s for project %s" % (e.message, self.service, self.targets, project['projectId']))

                except Exception as e:
                    printException(e)

        except HttpError as e:
            error_json = json.loads(e.content)
            if error_json['error']['message'] not in error_list:
                error_list.append(error_json['error']['message'])
                printError(error_json['error']['message'])

        except Exception as e:
            printException(e)

        finally:
            return targets
