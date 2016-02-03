#!/usr/bin/env python

# Import stock packages
import datetime
import dateutil
import sys

# Import opinel
try:
    from opinel.utils import *
    from opinel.utils_ec2 import *
    from opinel.utils_iam import *
    from opinel.utils_sts import *
except Exception as e:
    print('Error: Scout2 now depends on the opinel package (previously AWSUtils submodule). Install all the requirements with the following command:')
    print('  $ pip install -r requirements.txt')

    sys.exit()

# Import Scout2 tools
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
    min_opinel, max_opinel = get_opinel_requirement()
    if not check_opinel_version(min_opinel):
        return 42

    # Create the list of services to analyze
    services = build_services_list(args.services, args.skipped_services)
    if not len(services):
        printError('Error: list of Amazon Web Services to be analyzed is empty.')
        return 42

    # Search for AWS credentials
    if not args.fetch_local:
        key_id, secret, token = read_creds(args.profile[0], args.csv_credentials[0], args.mfa_serial[0], args.mfa_code[0])
        if key_id is None:
            return 42

    # If local analysis, overwrite results
    if args.fetch_local:
        args.force_write = True

    # Set the environment name
    environment_name = get_environment_name(args)[0]

    ##### Load local data first
    aws_config = {}
    manage_dictionary(aws_config, 'services', {})
    for service in build_services_list():
        if service not in services or args.fetch_local or args.resume:
            aws_config['services'][service] = load_info_from_json(service, environment_name)
        else:
            # Reload data in specific cases...
            if service == 's3' and (args.bucket_name or args.skipped_bucket_name):
                aws_config['services'][service] = load_info_from_json(service, environment_name)
            # TODO: when working on a subset of available regions, reload data for other regions (reload all and kill selected regions)

    ##### Fetch all requested services' configuration
    for service in services:
        method = globals()['get_' + service + '_info']
        manage_dictionary(aws_config['services'], service, {})
        manage_dictionary(aws_config['services'][service], 'violations', {})
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
                    method_args['s3_params']['checked_buckets'] = args.bucket_name
                    method_args['s3_params']['skipped_buckets'] = args.skipped_bucket_name
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

    # For analyzis purposes, update the list of services to be the union of the fetched and loaded configurations
    services = build_services_list(args.services, args.skipped_services, aws_config)

    # Search for an existing ruleset if the environment is set
    if environment_name and args.ruleset_name == 'default':
        ruleset_name = search_ruleset(environment_name)
    else:
        ruleset_name = args.ruleset_name

    # Load findings from JSON config files
    ruleset = load_ruleset(ruleset_name)
    rules = init_rules(ruleset, services, environment_name, args.ip_ranges)

    ##### VPC analyzis
    analyze_vpc_config(aws_config, args.ip_ranges, args.ip_ranges_key_name)
    if 'ec2' in services:
        analyze_ec2_config(aws_config['services']['ec2'], aws_config['account_id'], args.force_write)

    ##### Multiple service analyzis
    if 'ec2' in services and 'iam' in services:
        try:
            match_instances_and_roles(aws_config['services']['ec2'], aws_config['services']['iam'])
        except Exception as e:
            printError('Error: EC2 or IAM configuration is missing.')
            printException(e)
    if 's3' in services and 'iam' in services:
        try:
            match_iam_policies_and_buckets(aws_config['services']['s3'], aws_config['services']['iam'])
        except Exception as e:
            printError('Error: s3 or IAM configuration is missing.')
            printException(e)

    # Single service analyzis
    printInfo('Analyzing AWS config...')
    for finding_path in rules:
        for rule in rules[finding_path]:
            printDebug('Processing %s rule: "%s"' % (finding_path.split('.')[0], rules[finding_path][rule]['description']))
            path = finding_path.split('.')
            service = path[0]
            manage_dictionary(aws_config['services'][service], 'violations', {})
            aws_config['services'][service]['violations'][rule] = {}
            aws_config['services'][service]['violations'][rule]['description'] =  rules[finding_path][rule]['description']
            aws_config['services'][service]['violations'][rule]['entities'] = rules[finding_path][rule]['entities']
            aws_config['services'][service]['violations'][rule]['level'] = rules[finding_path][rule]['level']
            if 'id_suffix' in rules[finding_path][rule]:
                aws_config['services'][service]['violations'][rule]['id_suffix'] = rules[finding_path][rule]['id_suffix']
            if 'display_path' in rules[finding_path][rule]:
                aws_config['services'][service]['violations'][rule]['display_path'] = rules[finding_path][rule]['display_path']
            try:
                aws_config['services'][service]['violations'][rule]['items'] = recurse(aws_config['services'], aws_config['services'], path, [], rules[finding_path][rule], True)
            except Exception as e:
                printError('Failed to process rule defined in %s.json' % rule)
                printException(e)
            aws_config['services'][service]['violations'][rule]['dashboard_name'] = rules[finding_path][rule]['dashboard_name'] if 'dashboard_name' in rules[finding_path][rule] else '??'
            aws_config['services'][service]['violations'][rule]['checked_items'] = rules[finding_path][rule]['checked_items'] if 'checked_items' in rules[finding_path][rule] else 0
            aws_config['services'][service]['violations'][rule]['flagged_items'] = len(aws_config['services'][service]['violations'][rule]['items'])
            aws_config['services'][service]['violations'][rule]['service'] = service

    # Tweaks
    if 'cloudtrail' in services:
        tweak_cloudtrail_findings(aws_config)

    # Save info about run
    aws_config['last_run'] = {}
    aws_config['last_run']['time'] = datetime.datetime.now(dateutil.tz.tzlocal()).strftime("%Y-%m-%d %H:%M%S%z")
    aws_config['last_run']['cmd'] = ' '.join(sys.argv)

    # Generate dashboard metadata
    create_report_metadata(aws_config, services)

    # Save data
    create_scout_report(environment_name, aws_config, args.force_write, args.debug)


########################################
##### Argument parser
########################################

default_args = read_profile_default_args(parser.prog)

add_sts_argument(parser, 'mfa-serial')
add_sts_argument(parser, 'mfa-code')
add_common_argument(parser, default_args, 'regions')
add_common_argument(parser, default_args, 'with-gov')
add_common_argument(parser, default_args, 'with-cn')
add_common_argument(parser, default_args, 'ip-ranges')
add_common_argument(parser, default_args, 'ip-ranges-key-name')
add_iam_argument(parser, default_args, 'csv-credentials')
add_s3_argument(parser, default_args, 'bucket-name')
add_s3_argument(parser, default_args, 'skipped-bucket-name')
add_scout2_argument(parser, default_args, 'force')
add_scout2_argument(parser, default_args, 'ruleset-name')
add_scout2_argument(parser, default_args, 'services')
add_scout2_argument(parser, default_args, 'skip')
add_scout2_argument(parser, default_args, 'env')

parser.add_argument('--local',
                    dest='fetch_local',
                    default=False,
                    action='store_true',
                    help='use local data previously fetched to feed the analyzer')
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
parser.add_argument('--resume',
                    dest='resume',
                    default=False,
                    action='store_true',
                    help='Complete a partial (throttled) run')

args = parser.parse_args()

if __name__ == '__main__':
    sys.exit(main(args))
