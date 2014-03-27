#!/usr/bin/env python2

# Import the Amazon SDK
import boto
import boto.ec2
import boto.vpc

# Import AWS Scout2 tools
from AWSScout2.utils import *
from AWSScout2.utils_ec2 import *
from AWSScout2.utils_iam import *
from AWSScout2.utils_s3 import *

# Import other third-party packages
import argparse
import os
import traceback


########################################
##### Main
########################################

def main(args):

    key_id = None
    secret = None
    session_token = None

    # Fetch credentials from the EC2 instance's metadata
    if args.fetch_creds_from_instance_metadata:
        key_id, secret = fetch_iam_role_credentials()

    # Fetch credentials from CSV
    if args.fetch_creds_from_csv is not None:
        key_id, secret = fetch_creds_from_csv(args.fetch_creds_from_csv[0])

    # Fetch credentials from environment
    if key_id is None and secret is None and 'AWS_ACCESS_KEY_ID' in os.environ and 'AWS_SECRET_ACCESS_KEY' in os.environ:
        key_id = os.environ["AWS_ACCESS_KEY_ID"]
        secret = os.environ["AWS_SECRET_ACCESS_KEY"]

    if not args.fetch_local and (key_id is None or secret is None):
        print 'Error: could not find AWS credentials. Use the --help option for more information.'
        return -1

    # Fetch STS credentials
    if args.mfa_code or args.mfa_serial:
        key_id, secret, session_token = fetch_sts_credentials(key_id, secret, args.mfa_serial, args.mfa_code)

    ##### IAM
    if args.fetch_iam:
        # Fetch data from AWS or an existing local file
        if not args.fetch_local:
            iam_info = get_iam_info(key_id, secret, session_token)
        else:
            iam_info = load_info_from_json('iam')
        # Analyze the EC2 config and save data to a local file
        analyze_iam_config(iam_info, args.force_write)

    ##### EC2
    if args.fetch_ec2:
        # Fetch data from AWS or an existing local file
        if not args.fetch_local:
            ec2_info = get_ec2_info(key_id, secret, session_token, args.fetch_ec2_gov)
        else:
            ec2_info = load_info_from_json('ec2')
        # Analyze the EC2 config and save data to a local file
        analyze_ec2_config(ec2_info, args.force_write)


    ##### S3
    if args.fetch_s3:
        if not args.fetch_local:
            s3_info = get_s3_info(key_id, secret, session_token)
        else:
            s3_info = load_info_from_json('s3')
        # Analyze the S3 config and save data to a local file
        analyze_s3_config(s3_info, args.force_write)


    ##### Analyzis that requires multiple configuration
    if args.fetch_ec2 and args.fetch_iam:
        match_instances_and_roles(ec2_info, iam_info)
        save_config_to_file(iam_info, 'iam', args.force_write)


########################################
##### Argument parser
########################################
parser = argparse.ArgumentParser()
parser.add_argument('--no_iam',
                    dest='fetch_iam',
                    default=True,
                    action='store_false',
                    help='don\'t fetch the IAM configuration')
parser.add_argument('--no_ec2',
                    dest='fetch_ec2',
                    default=True,
                    action='store_false',
                    help='don\'t fetch the EC2 configuration')
parser.add_argument('--no_s3',
                    dest='fetch_s3',
                    default='True',
                    action='store_false',
                    help='don\'t fetch the S3 configuration')
parser.add_argument('--gov',
                    dest='fetch_ec2_gov',
                    default=False,
                    action='store_true',
                    help='fetch the EC2 configuration from the us-gov-west-1 region')
parser.add_argument('--force',
                    dest='force_write',
                    default=False,
                    action='store_true',
                    help='overwrite existing json files')
parser.add_argument('--role-credentials',
                    dest='fetch_creds_from_instance_metadata',
                    default=False,
                    action='store_true',
                    help='fetch credentials for this EC2 instance')
parser.add_argument('--credentials',
                    dest='fetch_creds_from_csv',
                    default=None,
                    nargs='+',
                    help='credentials file')
parser.add_argument('--mfa_serial',
                    dest='mfa_serial',
                    default=None,
                    nargs='+',
                    help='MFA device\'s serial number')
parser.add_argument('--mfa_code',
                    dest='mfa_code',
                    default=None,
                    nargs='+',
                    help='MFA code')
parser.add_argument('--local',
                    dest='fetch_local',
                    default=False,
                    action='store_true',
                    help='Use local data previously fetched to feed the analyzer')

args = parser.parse_args()

if __name__ == '__main__':
    main(args)
