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
from AWSScout2.utils_vpc import *

# Import other third-party packages
import argparse
import os

# Set two environment variables as required by Boto
#os.environ["AWS_ACCESS_KEY_ID"] = 'XXXXX'
#os.environ["AWS_SECRET_ACCESS_KEY"] = 'XXXXX'


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
        try:
            if not args.fetch_local:
                iam = boto.connect_iam(aws_access_key_id = key_id, aws_secret_access_key = secret, security_token = session_token)
                permissions = {}
                print 'Fetching IAM users data...'
                users, permissions = get_users_info(iam, permissions)
                save_to_file(users, 'IAM users', args.force_write)
                print 'Fetching IAM groups data...'
                groups, permissions = get_groups_info(iam, permissions)
                save_to_file(groups, 'IAM groups', args.force_write)
                print 'Fetching IAM roles data...'
                roles, permissions = get_roles_info(iam, permissions)
                save_to_file(roles, 'IAM roles', args.force_write)
                p = {}
                p['permissions'] = permissions
                save_to_file(p, 'IAM permissions', args.force_write)
            else:
                groups = load_from_json('iam','groups')
                permissions = load_from_json('iam','permissions')
                roles = load_from_json('iam','roles')
                users = load_from_json('iam','users')
            analyze_iam_config(groups, permissions, roles, users, args.force_write)
        except Exception, e:
            print 'Exception:\n %s' % e
            pass

    ##### EC2
    if args.fetch_ec2:
        security_groups = {}
        instances = {}
        try:
            if not args.fetch_local:
                for region in boto.ec2.regions():
                    try:
                        ec2_connection = boto.ec2.connect_to_region(region.name, aws_access_key_id = key_id, aws_secret_access_key = secret, security_token = session_token)
                        if region.name != 'us-gov-west-1' or args.fetch_ec2_gov:
                            print 'Fetching EC2 security groups data for region %s...' % region.name
                            manage_dictionary(security_groups, region.name, {})
                            security_groups[region.name].update(get_security_groups_info(ec2_connection, region.name))
                            print 'Fetching EC2 instances data for region %s...' % region.name
                            instances.update(get_instances_info(ec2_connection, region.name))
                    except Exception, e:
                        print 'Exception: Failed to fetch EC2 data for region %s\n %s' % (region.name, e)
                        pass
                save_to_file(security_groups, 'EC2 security groups', args.force_write)
                save_to_file(instances, 'EC2 instances', args.force_write)
            else:
                instances = load_from_json('ec2', 'instances')
                security_groups = load_from_json('ec2', 'security_groups')
            analyze_ec2_config(instances, security_groups, args.force_write)
        except Exception, e:
            print 'Exception: \n %s' % e
            pass

    ##### S3
    if args.fetch_s3:
        buckets = {}
        buckets['buckets'] = []
        try:
            if not args.fetch_local:
                s3_connection = boto.connect_s3(aws_access_key_id = key_id, aws_secret_access_key = secret, security_token = session_token)
                print 'Fetching S3 buckets data...'
                buckets['buckets'] = get_s3_buckets(s3_connection)
                save_to_file(buckets, 'S3 buckets', args.force_write)
            else:
                buckets = load_from_json('s3', 'buckets')
            analyze_s3_config(buckets, args.force_write)
        except Exception, e:
            print 'Exception: \n %s' % e
            pass

    ##### VPC
    if args.fetch_vpc:
        vpcs = {}
        try:
            if not args.fetch_local:
                for region in boto.ec2.regions():
                    if region.name != 'us-gov-west-1' or args.fetch_ec2_gov:
                        try:
                            manage_dictionary(vpcs, region.name, {})
                            vpc_connection = boto.vpc.connect_to_region(aws_access_key_id = key_id, aws_secret_access_key = secret, security_token = session_token, region_name = region.name)
                            print 'Fetching network ACLs data for region %s...' % region.name
                            vpcs[region.name].update(get_vpc_info(vpc_connection))
                        except Exception, e:
                            print 'Exception: \n %s' % e
                            pass
                save_to_file(vpcs, 'VPC network ACLs', args.force_write)
        except Exception, e:
            print 'Exception: \n %s' % e
            pass



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
parser.add_argument('--no_vpc',
                    dest='fetch_vpc',
                    default='True',
                    action='store_false',
                    help='don\'t fetch the VPC configuration')
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
