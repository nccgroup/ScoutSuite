#!/usr/bin/env python2

# Import third-party packages
import os
import sys

# Import AWS Utils
try:
    from AWSUtils.utils import *
    from AWSUtils.utils_ec2 import *
    from AWSUtils.utils_iam import *
except:
    print 'Error: Scout2 now depends on the AWS Utils module. Update your local repository with the following commands:'
    print '  $ git submodule init'
    print '  $ git submodule update'
    sys.exit()

# Import Scout2 tools
from AWSScout2.filters import *
from AWSScout2.findings import *
from AWSScout2.utils_cloudtrail import * 
from AWSScout2.utils_ec2 import *
from AWSScout2.utils_iam import *
from AWSScout2.utils_rds import *
from AWSScout2.utils_s3 import *


########################################
##### Main
########################################

def main(args):

    key_id = None
    secret = None
    mfa_serial = None
    session_token = None

    # Configure the debug level
    configPrintException(args.debug)

    # Create the list of services to analyze
    services = build_services_list(args.services, args.skipped_services)
    if not len(services):
        print 'Error: list of Amazon Web Services to be analyzed is empty.'
        return -1

    # Check the version of boto
    if not args.fetch_local and not check_boto_version():
        return -1

    # Fetch credentials
    key_id, secret, token = read_creds(args.profile[0], args.fetch_creds_from_csv[0], args.mfa_serial[0], args.mfa_code[0])

    # Check that credentials, if required, are available
    if not args.fetch_local and key_id is None:
        print 'Error: could not find AWS credentials. Use the --help option for more information.'
        return -1

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

    ##### CloudTrail
    if 'cloudtrail' in services:
        try:
            # Fetch data from AWS or an existing local file
            if not args.fetch_local:
                cloudtrail_info = get_cloudtrail_info(key_id, secret, token, args.regions)
            else:
                cloudtrail_info = load_info_from_json('cloudtrail', environment_name)
            # Analyze the CloudTrail config and save data to a local file
            analyze_cloudtrail_config(cloudtrail_info, args.force_write)
        except Exception, e:
            print 'Error: could not fetch and/or analyze CloudTrail configuration'
            printException(e)

    ##### IAM
    if 'iam' in services:
        iam_info = {}
        try:
            # Fetch data from local file
            if args.fetch_local or args.resume:
                iam_info = load_info_from_json('iam', environment_name)
            # Fetch data from AWS
            if not args.fetch_local:
                get_iam_info(key_id, secret, token, iam_info)
        except Exception, e:
            print 'Error: could not fetch IAM configuration'
            printException(e)
        try:
            # Analyze the IAM config and save data to a local file
            if 'ec2' not in services:
                analyze_iam_config(iam_info, args.force_write)
        except Exception, e:
            print 'Error: could not analyze IAM configuration'
            printException(e)

    ##### EC2
    if 'ec2' in services:
        try:
            # Fetch data from AWS or an existing local file
            if not args.fetch_local:
                ec2_info = get_ec2_info(key_id, secret, token, args.regions, args.fetch_gov)
            else:
                ec2_info = load_info_from_json('ec2', environment_name)
            # Analyze the EC2 config and save data to a local file
            analyze_ec2_config(ec2_info, args.force_write)
        except Exception, e:
            print 'Error: could not fetch and/or analyze EC2 configuration'
            printException(e)

    ##### RDS
    if 'rds' in services:
        try:
            if not args.fetch_local:
                rds_info = get_rds_info(key_id, secret, token, args.regions, args.fetch_gov)
            else:
                rds_info = load_info_from_json('rds', environment_name)
            analyze_rds_config(rds_info, args.force_write)
        except Exception, e:
            print 'Error: could not fetch and/or analyze RDS configuration'
            printException(e)

    ##### S3
    if 's3' in services:
        try:
            if not args.fetch_local:
                # If working on a subset of buckets, attempt to load an existing configuration dump to complete it
                if args.buckets or args.skipped_buckets:
                    try:
                        s3_info = load_info_from_json('s3', environment_name)
                    except Exception, e:
                        pass
                else:
                    s3_info = {}
                s3_params = {}
                s3_params['check_encryption'] = args.check_s3_encryption
                s3_params['check_acls'] = args.check_s3_acls
                s3_params['checked_buckets'] = args.buckets
                s3_params['skipped_buckets'] = args.skipped_buckets
                get_s3_info(key_id, secret, token, s3_info, s3_params)
            else:
                s3_info = load_info_from_json('s3', environment_name)
            # Analyze the S3 config and save data to a local file
            analyze_s3_config(s3_info, args.force_write)
        except Exception, e:
            print 'Error: could not fetch and/or analyze S3 configuration'
            printException(e)

    ##### Analyzis that requires multiple configuration
    if 'ec2' in services and 'iam' in services:
        try:
            match_instances_and_roles(ec2_info, iam_info)
            analyze_iam_config(iam_info, args.force_write)
        except Exception, e:
            print 'Error: EC2 or IAM configuration is missing'
            printException(e)

    ##### Rename data based on environment's name
    if environment_name:
        create_new_scout_report(environment_name, args.force_write)


########################################
##### Argument parser
########################################

init_parser()
parser.add_argument('--gov',
                    dest='fetch_gov',
                    default=False,
                    action='store_true',
                    help='fetch the EC2 configuration from the us-gov-west-1 region')
parser.add_argument('--csv_credentials',
                    dest='fetch_creds_from_csv',
                    default=[ None ],
                    nargs='+',
                    help='fetch credentials from a CSV file')
parser.add_argument('--mfa_serial',
                    dest='mfa_serial',
                    default=[ None ],
                    nargs='+',
                    help='MFA device\'s serial number')
parser.add_argument('--mfa_code',
                    dest='mfa_code',
                    default=[ None ],
                    nargs='+',
                    help='MFA code')
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
parser.add_argument('--check_s3_encryption',
                    dest='check_s3_encryption',
                    default=False,
                    action='store_true',
                    help='Pulls server-side encryption settings for each object in bucket (Slow)')
parser.add_argument('--check_s3_acls',
                    dest='check_s3_acls',
                    default=False,
                    action='store_true',
                    help='Pulls permissions for each object in bucket (Slow)')
parser.add_argument('--skip_buckets',
                    dest='skipped_buckets',
                    default=[],
                    nargs='+',
                    help='Name of S3 buckets to skip when checking object properties')
parser.add_argument('--buckets',
                    dest='buckets',
                    default=[],
                    nargs='+',
                    help='Name of buckets to iterate through when checking object properties')
parser.add_argument('--resume',
                    dest='resume',
                    default=False,
                    action='store_true',
                    help='Loads partial data before and only fetches missing data. Useful when throttling errors occured.')
parser.add_argument('--regions',
                    dest='regions',
                    default=[],
                    nargs='+',
                    help='Name of the regions to fetch the data from')

args = parser.parse_args()

if __name__ == '__main__':
    main(args)
