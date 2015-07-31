#!/usr/bin/env python2

# Import opinel
from opinel.utils import *
from opinel.utils_rds import *
from opinel.protocols_dict import *

# Import AWS Scout2 tools
from AWSScout2.utils import *
from AWSScout2.filters import *
from AWSScout2.findings import *


########################################
##### RDS functions
########################################

def analyze_rds_config(rds_info, force_write):
    printInfo('Analyzing RDS data...')
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
    for region in build_region_list('rds', selected_regions, include_gov = fetch_gov):
        rds_info['regions'][region] = {}
        rds_info['regions'][region]['name'] = region
    thread_work((key_id, secret, session_token), rds_info, rds_info['regions'], get_rds_region)
    return rds_info

def get_rds_region(connection_info, q, params):
    key_id, secret, session_token = connection_info
    while True:
        try:
            rds_info, region = q.get()
            rds_client = connect_rds(key_id, secret, session_token, region)
            get_security_groups_info(rds_client, rds_info['regions'][region])
            get_instances_info(rds_client, rds_info['regions'][region])
        except Exception as e:
            printException(e)
            pass
        finally:
            q.task_done()

def get_security_groups_info(rds_client, region_info):
    groups = rds_client.describe_db_security_groups()['DBSecurityGroups']
    manage_dictionary(region_info, 'security_groups', {})
    for group in groups:
        region_info['security_groups'][group['DBSecurityGroupName']] = parse_security_group(group)

def parse_security_group(group):
    security_group = {}
    vpc_id = group['VpcId'] if 'VpcId' in group else 'no-vpc'
    security_group['name'] = group['DBSecurityGroupName']
    security_group['description'] = group['DBSecurityGroupDescription']
    security_group['ec2_groups'] = group['EC2SecurityGroups']
    security_group['ip_ranges'] = group['IPRanges']
    return security_group

def get_instances_info(rds_client, region_info):
    manage_dictionary(region_info, 'instances', {})
    dbinstances = rds_client.describe_db_instances()['DBInstances']
    total = 0
    for dbi in dbinstances:
        dbi_info = {}
        total = total + len(dbinstances)
        for key in ['DBInstanceIdentifier', 'InstanceCreateTime', 'Engine', 'DBInstanceStatus', 'AutoMinorVersionUpgrade', 'DBInstanceClass', 'MultiAZ', 'Endpoint', 'BackupRetentionPeriod', 'PubliclyAccessible', 'StorageEncrypted']:
            # parameter_groups , security_groups, vpc_security_gropus
            dbi_info[key] = dbi[key]
        region_info['instances'][dbi['DBInstanceIdentifier']] = dbi_info
