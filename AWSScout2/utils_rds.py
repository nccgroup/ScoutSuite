#!/usr/bin/env python2

# Import the Amazon SDK
import boto
from boto.rds import *

# Import AWS Scout2 tools
from AWSScout2.utils import *
from AWSScout2.filters import *
from AWSScout2.findings import *
from AWSScout2.protocols_dict import *


########################################
##### RDS functions
########################################

def analyze_rds_config(rds_info, force_write):
    print 'Analyzing RDS data...'
    analyze_config(rds_finding_dictionary, rds_filter_dictionary, rds_info, 'RDS', force_write)
    # Custom RDS analysis
    check_for_duplicate(rds_info)
    save_config_to_file(rds_info, 'RDS', force_write)

def check_for_duplicate(rds_info):
    # Backup disabled also triggers short-backup-retention, remove duplicates
    if 'short-backup-retention-period' in rds_info['violations']:
        if 'backup-disabled' in rds_info['violations']:
            for instance_id in rds_info['violations']['backup-disabled'].items:
                rds_info['violations']['short-backup-retention-period'].removeItem(instance_id)

def get_rds_info(key_id, secret, session_token, fetch_gov):
    rds_info = {}
    rds_info['regions'] = {}
    build_region_list(boto.rds.regions(), rds_info, fetch_gov)
    for region in rds_info['regions']:
        try:
            print 'Fetching RDS data for region %s...' % region
            rds_connection = boto.rds.connect_to_region(region, aws_access_key_id = key_id, aws_secret_access_key = secret, security_token = session_token)
            get_security_groups_info(rds_connection, rds_info['regions'][region])
            get_instances_info(rds_connection, rds_info['regions'][region])

        except Exception, e:
            printException(e)
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
        owner_id = ec2_group.owner_id
        if not owner_id:
            owner_id = 'unknown'
        manage_dictionary(security_group['ec2_groups']['owners'], owner_id, {})
        manage_dictionary(security_group['ec2_groups']['owners'][owner_id], 'groups', [])
        security_group['ec2_groups']['owners'][owner_id]['groups'].append(ec2_group.name)
    security_group['ip_ranges'] = []
    for ip in group.ip_ranges:
        security_group['ip_ranges'].append(ip.cidr_ip)
    return security_group

def get_instances_info(rds_connection, region_info):
    manage_dictionary(region_info, 'instances', {})
    dbinstances = rds_connection.get_all_dbinstances()
    count, total = init_status(None, 'Instances')
    for dbi in dbinstances:
        dbi_info = {}
        total = total + len(dbinstances)
        for key in ['id', 'create_time', 'engine', 'status', 'auto_minor_version_upgrade', 'instance_class', 'multi_az', 'endpoint', 'backup_retention_period', 'PubliclyAccessible']:
            # parameter_groups , security_groups, vpc_security_gropus
            dbi_info[key] = dbi.__dict__[key]
        region_info['instances'][dbi.id] = dbi_info
        count = update_status(count, total, 'Instances')
    close_status(count, total, 'Instances')
