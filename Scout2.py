#!/usr/bin/env python

# Import third-party packages
import os
import sys

# Import opinel
try:
    from opinel.utils import *
    from opinel.utils_ec2 import *
    from opinel.utils_iam import *
    from opinel.utils_sts import *
except:
    print('Error: Scout2 now depends on the opinel package (previously AWSUtils submodule). Install all the requirements with the following command:')
    print('  $ pip install -r requirements.txt')
    sys.exit()

# Import Scout2 tools
from AWSScout2.filters import *
from AWSScout2.findings import *
from AWSScout2.utils_cloudtrail import *
from AWSScout2.utils_ec2 import *
from AWSScout2.utils_iam import *
from AWSScout2.utils_rds import *
from AWSScout2.utils_redshift import *
from AWSScout2.utils_s3 import *
from AWSScout2.utils_vpc import *


########################################
##### Main
########################################

def main(args):

    # Configure the debug level
    configPrintException(args.debug)

    # Check version of opinel
    # TODO: read version from requirements
    if not check_opinel_version('0.11.0'):
        return 42

    # Create the list of services to analyze
    services = build_services_list(args.services, args.skipped_services)
    if not len(services):
        printError('Error: list of Amazon Web Services to be analyzed is empty.')
        return 42

    # Search for AWS credentials
    key_id, secret, token = read_creds(args.profile[0], args.fetch_creds_from_csv[0], args.mfa_serial[0], args.mfa_code[0])
    if not args.fetch_local and key_id is None:
        return 42

    # If local analysis, overwrite results
    if args.fetch_local:
        args.force_write = True

    # Set the environment name
    environment_name = get_environment_name(args)

    # Search for an existing ruleset if the environment is set
    if environment_name and args.ruleset_name == 'default':
        ruleset_name = search_ruleset(environment_name)
    else:
        ruleset_name = args.ruleset_name

    # Load findings from JSON config files
    for service in services:
        load_findings(service, ruleset_name)
        load_filters(service)

    ##### Load local data first
    aws_config = {}
    manage_dictionary(aws_config, 'services', {})
    for service in build_services_list():
        if service not in services or args.fetch_local or args.resume:
            aws_config['services'][service] = load_info_from_json(service, environment_name)
        else:
            # Reload data in specific cases...
            if service == 's3' and (args.buckets or args.skipped_buckets):
                aws_config['services'][service] = load_info_from_json(service, environment_name)
            # TODO: when working on a subset of available regions, reload data for other regions (reload all and kill selected regions)

    ##### Fetch all requested services' configuration
    for service in services:
        method = globals()['get_' + service + '_info']
        manage_dictionary(aws_config['services'], service, {})
        try:
            if not args.fetch_local:
                # Fetch data from AWS API
                method_args = {}
                method_args['key_id'] = key_id
                method_args['secret'] = secret
                method_args['session_token'] = token
                method_args['service_config'] = aws_config['services'][service]
                if service != 'iam':
                    method_args['selected_regions'] = args.regions
                    method_args['with_gov'] = args.with_gov
                    method_args['with_cn'] = args.with_cn
                if service == 's3':
                    method_args['s3_params'] = {}
                    method_args['s3_params']['check_encryption'] = args.check_s3_encryption
                    method_args['s3_params']['check_acls'] = args.check_s3_acls
                    method_args['s3_params']['checked_buckets'] = args.buckets
                    method_args['s3_params']['skipped_buckets'] = args.skipped_buckets
                method(**method_args)
            else:
                # Fetch data from a local file
                aws_config['services'][service] = load_info_from_json(service, environment_name)
        except Exception as e:
            printError('Error: could not fetch %s configuration.' % service)
            printException(e)

    ##### Save this AWS account ID
    if 'iam' in services and (not 'account_id' in aws_config or not aws_config['account_id']):
        aws_config['account_id'] = get_aws_account_id(aws_config['services']['iam'])
    else:
        manage_dictionary(aws_config, 'account_id', None)

    ##### Single service analyzis
    for service in services:
        method = globals()['analyze_' + service + '_config']
        method(aws_config['services'][service], aws_config['account_id'], args.force_write)

    ##### Multiple service analyzis
    if 'ec2' in services and 'iam' in services:
        try:
            match_instances_and_roles(aws_config['services']['ec2'], aws_config['services']['iam'])
        except Exception as e:
            printError('Error: EC2 or IAM configuration is missing.')
            printException(e)

    ##### VPC analyzis
    analyze_vpc_config(aws_config)

    # Save data
    save_config_to_file(aws_config, 'aws', args.force_write, args.debug)

    ##### Rename data based on environment's name
    if environment_name:
        create_new_scout_report(environment_name, args.force_write)


########################################
##### Argument parser
########################################

default_args = read_profile_default_args(parser.prog)

add_sts_argument(parser, 'mfa-serial')
add_sts_argument(parser, 'mfa-code')
add_common_argument(parser, default_args, 'regions')
add_common_argument(parser, default_args, 'with-gov')
add_common_argument(parser, default_args, 'with-cn')
add_scout2_argument(parser, default_args, 'force')
add_scout2_argument(parser, default_args, 'ruleset-name')
add_scout2_argument(parser, default_args, 'services')
add_scout2_argument(parser, default_args, 'skip')

parser.add_argument('--csv-credentials',
                    dest='fetch_creds_from_csv',
                    default=[ None ],
                    nargs='+',
                    help='fetch credentials from a CSV file')
parser.add_argument('--local',
                    dest='fetch_local',
                    default=False,
                    action='store_true',
                    help='use local data previously fetched to feed the analyzer')
parser.add_argument('--env',
                    dest='environment_name',
                    default=None,
                    nargs='+',
                    help='AWS environment name (used to create multiple reports)')
parser.add_argument('--check-s3-acls',
                    dest='check_s3_acls',
                    default=False,
                    action='store_true',
                    help='Pulls permissions for each object in bucket (Slow)')
parser.add_argument('--check-s3-encryption',
                    dest='check_s3_encryption',
                    default=False,
                    action='store_true',
                    help='Pulls server-side encryption settings for each object in bucket (Slow)')
parser.add_argument('--buckets',
                    dest='buckets',
                    default=[],
                    nargs='+',
                    help='Name of buckets to iterate through when checking object properties')
parser.add_argument('--skipped-buckets',
                    dest='skipped_buckets',
                    default=[],
                    nargs='+',
                    help='Name of S3 buckets to skip when checking object properties')
parser.add_argument('--resume',
                    dest='resume',
                    default=False,
                    action='store_true',
                    help='Complete a partial (throttled) run')

args = parser.parse_args()

if __name__ == '__main__':
    sys.exit(main(args))
