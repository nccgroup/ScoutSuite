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

    def __init__(self):
        self.account_id = None
        self.last_run = None
        self.metadata = None
        self.services = ServicesConfig()
        self.ruleset = None

    def load_metadata(self):
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




