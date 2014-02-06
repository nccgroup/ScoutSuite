#!/usr/bin/env python

# Import the Amazon SDK
import boto
import boto.ec2

# Import AWS Scout2 tools
from AWSScout2.utils import *
from AWSScout2.utils_ec2 import *
from AWSScout2.utils_iam import *
from AWSScout2.utils_s3 import *

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

    # Fetch credentials from the EC2 instance's metadata
    if args.fetch_creds_from_instance_metadata:
        key_id, secret = fetch_iam_role_credentials()

    # Fetch credentials from CSV
    if args.fetch_creds_from_csv is not None:
        key_id, secret = fetch_creds_from_csv(args.fetch_creds_from_csv[0])

    # Fetch credentials from environment
    if 'AWS_ACCESS_KEY_ID' in os.environ and 'AWS_SECRET_ACCESS_KEY' in os.environ:
        key_id = os.environ["AWS_ACCESS_KEY_ID"]
        secret = os.environ["AWS_SECRET_ACCESS_KEY"] = secret

    if key_id is None or secret is None:
        print 'Error: you need to set your AWS credentials as environment variables to use Scout2.'
        return -1

    ##### IAM
    if args.fetch_iam:
        try:
            iam = boto.connect_iam(key_id, secret)
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
            analyze_iam_config(groups, permissions, roles, users)
        except Exception, e:
            print 'Exception:\n %s' % e
            pass

    ##### EC2
    if args.fetch_ec2:
      security_groups = {}
      security_groups['security_groups'] = []
      instances = {}
      instances['instances'] = []
      for region in boto.ec2.regions():
          ec2_connection = boto.ec2.connect_to_region(region.name, aws_access_key_id = key_id, aws_secret_access_key = secret)
          if region.name != 'us-gov-west-1' or args.fetch_ec2_gov:
            try:
                print 'Fetching EC2 data for region %s' % region.name
                security_groups['security_groups'] += get_security_groups_info(ec2_connection, region.name)
                instances['instances'] += get_instances_info(ec2_connection, region.name)
            except Exception, e:
                print 'Exception: \n %s' % e
                pass
      save_to_file(security_groups, 'EC2 security groups', args.force_write)
      save_to_file(instances, 'EC2 instances', args.force_write)
      analyze_ec2_config(instances, security_groups)

    ##### S3
    if args.fetch_s3:
        buckets = {}
        buckets['buckets'] = []
        s3_connection = boto.connect_s3(key_id, secret)
        print 'Fetching S3 buckets data...'
        buckets['buckets'] = get_s3_buckets(s3_connection)
        save_to_file(buckets, 'S3 buckets', args.force_write)
        analyze_s3_config(buckets)


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

args = parser.parse_args()

if __name__ == '__main__':
    main(args)
