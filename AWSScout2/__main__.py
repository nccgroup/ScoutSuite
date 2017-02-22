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
from AWSScout2.exceptions import process_exceptions
from AWSScout2.Ruleset import Ruleset
from AWSScout2.Scout2Config import Scout2Config
from AWSScout2.ServicesConfig import postprocessing
from AWSScout2.postprocessing import do_postprocessing
from AWSScout2.utils import create_scout_report
from AWSScout2.cli_parser import Scout2ArgumentParser
from AWSScout2.fs import Scout2Report


########################################
##### Main
########################################

def main():

    parser = Scout2ArgumentParser()
    args = parser.parse_args()

    # Configure the debug level
    configPrintException(args.debug)

    # Setup timestamp if needed
    current_time = datetime.datetime.now(dateutil.tz.tzlocal())
    timestamp = args.timestamp
    if timestamp != False:
        timestamp = args.timestamp if args.timestamp else current_time.strftime("%Y-%m-%d_%Hh%M%z")

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
    report = Scout2Report(environment_name, args.report_dir, timestamp)
    aws_config = Scout2Config(args.services, args.skipped_services)

    # Blah
    if not args.fetch_local:
        # Fetch data from AWS APIs
        aws_config.fetch(credentials, regions=args.regions, partition_name=args.partition_name)
        aws_config.update_metadata()
        # Create a report
        report.save(aws_config, {}, args.force_write, args.debug)

    # Reload to flatten everything into a python dictionary
    aws_config = report.load()

    # Analyze config
    ruleset = Ruleset(environment_name)
    ruleset.analyze(aws_config)

    # Create display filters
    filters = Ruleset(ruleset_filename = 'rulesets/filters.json', rule_type = 'filters')
    filters.analyze(aws_config)
    #   filters = init_rules(filters, services, environment_name, args.ip_ranges, aws_config['account_id'],                         rule_type='filters')

    # Finalize
    postprocessing(aws_config)
    do_postprocessing(aws_config)

    # Handle exceptions
    process_exceptions(aws_config, args.exceptions[0])

    # Save config and create HTML report
    report.save(aws_config, {}, args.force_write, args.debug)
