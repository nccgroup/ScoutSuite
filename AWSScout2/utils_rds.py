#!/usr/bin/env python2

# Import AWS Scout2 tools
from AWSUtils.utils import *
from AWSUtils.utils_rds import *
from AWSUtils.protocols_dict import *

# Import AWS Scout2 tools
from AWSScout2.utils import *
from AWSScout2.filters import *
from AWSScout2.findings import *

# Import third-party packages
import boto
from boto import rds


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

def get_rds_info(key_id, secret, session_token, selected_regions, fetch_gov):
    rds_info = {}
    rds_info['regions'] = {}
    for region in build_region_list(boto.rds.regions(), selected_regions, include_gov = fetch_gov):
        rds_info['regions'][region] = {}
        rds_info['regions'][region]['name'] = region
    thread_work((key_id, secret, session_token), rds_info, rds_info['regions'], get_rds_region, show_status)
    return rds_info

def get_rds_region(connection_info, q, params):
    key_id, secret, session_token = connection_info
    while True:
        try:
            rds_info, region = q.get()
            rds_connection = connect_rds(key_id, secret, session_token, region)
            get_security_groups_info(rds_connection, rds_info['regions'][region])
            get_instances_info(rds_connection, rds_info['regions'][region])
        except Exception, e:
            printException(e)
            pass
        finally:
            q.task_done()

def get_security_groups_info(rds_connection, region_info):
    groups = rds_connection.get_all_dbsecurity_groups()
    manage_dictionary(region_info, 'security_groups', {})
    for group in groups:
        region_info['security_groups'][group.name] = parse_security_group(group)

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
    total = 0
    for dbi in dbinstances:
        dbi_info = {}
        total = total + len(dbinstances)
        for key in ['id', 'create_time', 'engine', 'status', 'auto_minor_version_upgrade', 'instance_class', 'multi_az', 'endpoint', 'backup_retention_period', 'PubliclyAccessible']:
            # parameter_groups , security_groups, vpc_security_gropus
            dbi_info[key] = dbi.__dict__[key]
        region_info['instances'][dbi.id] = dbi_info

def show_status(rds_info, stop_event):
    print 'Fetching RDS data...'
    while(not stop_event.is_set()):
        # This one is quiet for now...
        stop_event.wait(1)
        pass
