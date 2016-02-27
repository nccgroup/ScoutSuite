#!/usr/bin/env python

# Import AWS Scout2 tools
from AWSScout2.utils import *

# Import third-party packages
import datetime
import dateutil.parser
import netaddr
import re
import sys


########################################
##### Config file
########################################

class Bunch(object):
  def __init__(self, adict):
    self.__dict__.update(adict)


########################################
##### Main
########################################

def main(cmd_args):

    # Configure the debug level
    configPrintException(cmd_args.debug)

    # Get the environment name
    environment_names = get_environment_name(cmd_args)

    # Support multiple environments
    for environment_name in environment_names:

        # Load arguments from config if specified
        if len(cmd_args.config):
            rule_metadata = {'filename': cmd_args.config[0], 'enabled': True, 'args': cmd_args.config_args}
            config = load_config_from_json(rule_metadata, environment_name, cmd_args.ip_ranges)
            if config:
                args = Bunch(config)
            else:
                return 42
        else:
            args = cmd_args
            config = {}
            config['conditions'] = args.conditions if hasattr(args, 'conditions') else []
            config['mapping'] = args.mapping if hasattr(args, 'mapping') else []
            config['keys'] = args.keys

        # Load the data
        aws_config = {}
        aws_config['services'] = {}
        for service in supported_services:
            try:
                aws_config['services'][service] = load_info_from_json(service, environment_name)
            except Exception as e:
                printException(e)

        # Recursion
        if type(args.path) == list:
            config['path'] = args.path[0]
        else:
            config['path'] = args.path
        target_path = config['path'].split('.')
        current_path = []
        resources = recurse(aws_config['services'], aws_config['services'], target_path, current_path, config)

        # Do a print here ...
        if 'keys' in config:
          for resource in resources:
            output = ''
            current_path = resource.split('.')
            for key in config['keys']:
                if not output:
                    output = get_value_at(aws_config['services'], current_path, key, True)
                else:
                    output = output + ', ' + get_value_at(aws_config['services'], current_path, key, True)
            printInfo(output)
        else:
            printInfo(json.dumps(resources, indent=4))

#            service = entity.pop(0)
#            if output_format != 'csv':
#                printInfo(output_format['header'])
#            list_all(aws_config, aws_config[service], entity, [ service ], args.keys, conditions, output_format, mapping)
#            if output_format != 'csv':
#                printInfo(output_format['footer'])


########################################
##### Argument parser
########################################

default_args = read_profile_default_args(parser.prog)

add_scout2_argument(parser, default_args, 'env')

parser.add_argument('--config',
                    dest='config',
                    default=[],
                    nargs='+',
                    help='Config file that sets the path and keys to be listed.')
parser.add_argument('--format',
                    dest='format',
                    default=['csv'],
                    nargs='+',
                    help='Bleh.')
parser.add_argument('--path',
                    dest='path',
                    default=[],
                    nargs='+',
                    help='Path of the resources to list (e.g. iam.users.id or ec2.regions.id.vpcs.id)')
parser.add_argument('--keys',
                    dest='keys',
                    default=[ 'this' ],
                    nargs='+',
                    help='Keys to be printed for the given object.')
parser.add_argument('--ip-ranges',
                    dest='ip_ranges',
                    default=[],
                    nargs='+',
                    help='Config file(s) that contain your own IP ranges.')
parser.add_argument('--config-args',
                    dest='config_args',
                    default=[],
                    nargs='+',
                    help='Arguments to be passed to the config file.')

args = parser.parse_args()

if __name__ == '__main__':
    sys.exit(main(args))
