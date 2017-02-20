# Import future stuff...
from __future__ import print_function
from __future__ import unicode_literals


import json

from AWSScout2.ServicesConfig import ServicesConfig
from AWSScout2.utils import *

class Scout2Config(object):
    """
    Root object that holds all of the necessary AWS resources and Scout2
    configuration items.

    :account_id         AWS account ID
    :last_run           Information about the last run
    :metadata           Metadata used to generate the HTML report
    :ruleset            Ruleset used to perform the analysis
    :services           AWS configuration sorted by service
    """

    def __init__(self, services = [], skipped_services = []):
        self.account_id = None
        self.last_run = None
        self.__load_metadata()
        supported_services = []
        for group in self.metadata:
            for service in self.metadata[group]:
                supported_services.append(service)
        self.service_list = self.build_services_list(supported_services, services, skipped_services)
        self.services = ServicesConfig()


    def fetch(self, credentials, regions = [], skipped_regions = [], partition_name = 'aws'):
        """

        :param credentials:
        :param services:
        :param skipped_services:
        :param regions:
        :param skipped_regions:
        :param partition_name:
        :return:
        """
        # TODO: determine partition name based on regions and warn if multiple partitions...

        self.services.fetch(credentials, self.service_list, regions, partition_name)


    def __load_metadata(self):
        # Load metadata
        with open('metadata.json', 'rt') as f:
            self.metadata = json.load(f)

    def save_to_file(self, environment_name, force_write = False, debug = False, js_filename = 'aws_config', js_varname = 'aws_info', quiet = False):
        print('Saving config to %s' % js_filename)
        try:
            with open_file(environment_name, force_write, js_filename, quiet) as f:
                print('%s =' % js_varname, file = f)
                print('%s' % json.dumps(vars(self), indent=4 if debug else None, separators=(',', ': '), sort_keys=True, cls=Scout2Encoder), file = f)
        except Exception as e:
            printException(e)
            pass

    def build_services_list(self, supported_services, services, skipped_services):
        return [s for s in supported_services if (services == [] or s in services) and s not in skipped_services]

