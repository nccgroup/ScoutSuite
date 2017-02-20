#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Import stock packages
import dateutil
import sys

# Import opinel
try:
    from opinel.utils import *
    from opinel.utils_ec2 import *
    from opinel.utils_iam import *
except Exception as e:
    print(e)
    print(
    'Error: Scout2 now depends on the opinel package (previously AWSUtils submodule). Install all the requirements with the following command:')
    print('  $ pip install -r requirements.txt')
    print(e)
    sys.exit(42)

# Import Scout2 tools
from AWSScout2 import __version__
from AWSScout2.utils_vpc import *
from AWSScout2.Ruleset import Ruleset
from AWSScout2.Scout2Config import Scout2Config
from AWSScout2.ServicesConfig import postprocessing
from AWSScout2.postprocessing import do_postprocessing
from AWSScout2.utils import create_scout_report


########################################
##### Main
########################################

def main(args):
    # Configure the debug level
    configPrintException(args.debug)

    # Setup timestamp if needed
    current_time = datetime.datetime.now(dateutil.tz.tzlocal())
    timestamp = args.timestamp
    if timestamp != False:
        timestamp = args.timestamp if args.timestamp else current_time.strftime("%Y-%m-%d_%Hh%M%z")

    # If local analysis, overwrite results
    if args.fetch_local:
        args.force_write = True

    # Check version of opinel
    min_opinel, max_opinel = get_opinel_requirement()
    if not check_opinel_version(min_opinel):
        return 42

    # Search for AWS credentials
    if not args.fetch_local:
        credentials = read_creds(args.profile[0], args.csv_credentials, args.mfa_serial, args.mfa_code)
        if credentials['AccessKeyId'] is None:
            return 42

    # Set the environment name
    # TODO FIX this as read-creds happens before
    environment_name = get_environment_name(args)[0]

    # Create a new Scout2 config
    new_config = Scout2Config(args.services, args.skipped_services)

    # Blah
    if not args.fetch_local:
        # Fetch data from AWS APIs
        new_config.fetch(credentials, regions=args.regions, partition_name=args.partition_name)
        new_config.update_metadata()
        # Save config file
        new_config.save_to_file(environment_name, args.force_write, args.debug)

    # Reload to flatten everything into a python dictionary
    aws_config = load_from_json(environment_name)

    # Analyze config
    ruleset = Ruleset(environment_name)
    ruleset.analyze(aws_config)

    # Filters
    filters = Ruleset(ruleset_filename = 'rulesets/filters.json', rule_type = 'filters')
    filters.analyze(aws_config)
    #   filters = init_rules(filters, services, environment_name, args.ip_ranges, aws_config['account_id'],                         rule_type='filters')

    # Finalize
    postprocessing(aws_config)
    do_postprocessing(aws_config)

    # Foobar

    #finalize(aws_config, current_time, sys.argv)

    # h4ck
    save_config_to_file(environment_name, aws_config, args.force_write, args.debug)

    create_scout_report(environment_name, timestamp, aws_config, {}, args.force_write, args.debug)
    return



    return

        ##### VPC analyzis
    #    analyze_vpc_config(aws_config, args.ip_ranges, args.ip_ranges_key_name)
    #    if 'ec2' in services:
    #        analyze_ec2_config(aws_config['services']['ec2'], aws_config['account_id'], args.force_write)
    #

    #    if 's3' in services and 'iam' in services:
    #        try:
    #            match_iam_policies_and_buckets(aws_config['services']['s3'], aws_config['services']['iam'])
    #        except Exception as e:
    #            printError('Error: s3 or IAM configuration is missing.')
    #            printException(e)






    # Exceptions
    exceptions = {}
    if args.exceptions[0]:
        with open(args.exceptions[0], 'rt') as f:
            exceptions = json.load(f)
        for service in exceptions['services']:
            for rule in exceptions['services'][service]['exceptions']:
                filtered_items = []
                for item in aws_config['services'][service]['violations'][rule]['items']:
                    if item not in exceptions['services'][service]['exceptions'][rule]:
                        filtered_items.append(item)
                aws_config['services'][service]['violations'][rule]['items'] = filtered_items
                aws_config['services'][service]['violations'][rule]['flagged_items'] = len(
                    aws_config['services'][service]['violations'][rule]['items'])


    # Generate dashboard metadata
    try:
        create_report_metadata(aws_config, services)
    except Exception as e:
        printError('Failed to create the report\'s dashboard metadata.')
        printException(e)

    # Save data
    create_scout_report(environment_name, timestamp, aws_config, exceptions, args.force_write, args.debug)


########################################
##### Argument parser
########################################

default_args = read_profile_default_args(parser.prog)

add_sts_argument(parser, 'mfa-serial')
add_sts_argument(parser, 'mfa-code')
add_common_argument(parser, default_args, 'regions')
add_common_argument(parser, default_args, 'partition-name')
add_common_argument(parser, default_args, 'ip-ranges')
add_common_argument(parser, default_args, 'ip-ranges-key-name')
add_iam_argument(parser, default_args, 'csv-credentials')
add_scout2_argument(parser, default_args, 'force')
add_scout2_argument(parser, default_args, 'ruleset')
add_scout2_argument(parser, default_args, 'services')
add_scout2_argument(parser, default_args, 'skip')
add_scout2_argument(parser, default_args, 'env')

parser.add_argument('--local',
                    dest='fetch_local',
                    default=False,
                    action='store_true',
                    help='use local data previously fetched to feed the analyzer')
parser.add_argument('--resume',
                    dest='resume',
                    default=False,
                    action='store_true',
                    help='Complete a partial (throttled) run')
parser.add_argument('--update',
                    dest='update',
                    default=False,
                    action='store_true',
                    help='Reload all the existing data and only overwrite data in scope for this run')
parser.add_argument('--exceptions',
                    dest='exceptions',
                    default=[None],
                    nargs='+',
                    help='')
parser.add_argument('--timestamp',
                    dest='timestamp',
                    default=False,
                    nargs='?',
                    help='Add a timestamp to the name of the report (default is current time in UTC)')

args = parser.parse_args()

if __name__ == '__main__':
    sys.exit(main(args))