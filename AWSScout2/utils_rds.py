#!/usr/bin/env python2

# Import the Amazon SDK
import boto
from boto.rds import *

# Import AWS Scout2 tools
from AWSScout2.utils import *
from AWSScout2.findings import *
from AWSScout2.protocols_dict import *

# Import other third-party packages
import traceback


########################################
##### RDS functions
########################################

def analyze_rds_config(rds_info, force_write):
    print 'Analyzing RDS data...'
    analyze_config(rds_finding_dictionary, rds_info, 'RDS', force_write)

def get_rds_info(key_id, secret, session_token, fetch_gov):
    rds_info = {}
    rds_info['regions'] = {}
    build_region_list(boto.rds.regions(), rds_info, fetch_gov)
    for region in rds_info['regions']:
        try:
            print 'Fetching RDS data for region %s...' % region
            rds_connection = boto.rds.connect_to_region(region, aws_access_key_id = key_id, aws_secret_access_key = secret, security_token = session_token)
            get_security_groups_info(rds_connection, rds_info['regions'][region])

        except Exception, e:
            print 'Exception:\n %s' % traceback.format_exc()
            pass
    return rds_info

def get_security_groups_info(rds_connection, region_info):
    groups = rds_connection.get_all_dbsecurity_groups()
    manage_dictionary(region_info, 'security_groups', {})
    count, total = init_status(groups, 'Security groups')
    for group in groups:
        region_info['security_groups'][group.name] = parse_security_group(group)
        count = update_status(count, total, 'Security groups')
    close_status(count, total, 'Security groups')

def parse_security_group(group):
    security_group = {}
    security_group['name'] = group.name
    security_group['description'] = group.description
    security_group['ec2_groups'] = {}
    security_group['ec2_groups']['owners'] = {}
    for ec2_group in group.ec2_groups:
        manage_dictionary(security_group['ec2_groups']['owners'], ec2_group.owner_id, {})
        manage_dictionary(security_group['ec2_groups']['owners'][ec2_group.owner_id], 'groups', [])
        security_group['ec2_groups']['owners'][ec2_group.owner_id]['groups'].append(ec2_group.name)
    security_group['ip_ranges'] = []
    for ip in group.ip_ranges:
        security_group['ip_ranges'].append(ip.cidr_ip)
    return security_group
