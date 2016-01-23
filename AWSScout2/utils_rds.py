
# Import opinel
from opinel.utils import *
from opinel.utils_rds import *

# Import AWS Scout2 tools
from AWSScout2.utils import *

########################################
##### RDS functions
########################################

def get_rds_info(key_id, secret, session_token, service_config, selected_regions, with_gov, with_cn):
    printInfo('Fetching RDS config...')
    manage_dictionary(service_config, 'regions', {})
    for region in build_region_list('rds', selected_regions, include_gov = with_gov, include_cn = with_cn):
        manage_dictionary(service_config['regions'], region, {})
        service_config['regions'][region]['name'] = region
    thread_work(service_config['regions'], get_rds_region, params = {'creds': (key_id, secret, session_token), 'rds_info': service_config})

def get_rds_region(q, params):
    key_id, secret, session_token = params['creds']
    rds_info = params['rds_info']
    while True:
        try:
            region = q.get()
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
    manage_dictionary(region_info, 'vpcs', {})
    manage_dictionary(region_info['vpcs'], ec2_classic, {})
    manage_dictionary(region_info['vpcs'][ec2_classic], 'security_groups', {})
    manage_dictionary(region_info, 'security_groups_count', 0)
    region_info['security_groups_count'] += len(groups)
    for group in groups:
        region_info['vpcs'][ec2_classic]['security_groups'][group['DBSecurityGroupName']] = parse_security_group(group)

def parse_security_group(group):
    security_group = {}
    security_group['name'] = group['DBSecurityGroupName']
    security_group['description'] = group['DBSecurityGroupDescription']
    security_group['ec2_groups'] = {}
    for grant in group['EC2SecurityGroups']:
        if 'EC2SecurityGroupId' in grant:
            group_id = grant.pop('EC2SecurityGroupId')
        else:
            group_id = '%s-%s' % (grant['EC2SecurityGroupOwnerId'], grant['EC2SecurityGroupName'])
        security_group['ec2_groups'][group_id] = grant
    security_group['ip_ranges'] = {}
    for ip_range in group['IPRanges']:
        cidr = ip_range.pop('CIDRIP')
        security_group['ip_ranges'][cidr] = ip_range
    return security_group

def get_instances_info(rds_client, region_info):
    manage_dictionary(region_info, 'vpcs', {})
    dbinstances = rds_client.describe_db_instances()['DBInstances']
    manage_dictionary(region_info, 'instances_count', 0)
    region_info['instances_count'] += len(dbinstances)
    total = 0
    for dbi in dbinstances:
        vpc_id = dbi['DBSubnetGroup']['VpcId'] if 'DBSubnetGroup' in dbi and 'VpcId' in dbi['DBSubnetGroup'] and dbi['DBSubnetGroup']['VpcId'] else ec2_classic
        manage_dictionary(region_info['vpcs'], vpc_id, {})
        manage_dictionary(region_info['vpcs'][vpc_id], 'instances', {})
        dbi_info = {}
        total = total + len(dbinstances)
        dbi_info['name'] = dbi.pop('DBInstanceIdentifier')
        for key in [ 'InstanceCreateTime', 'Engine', 'DBInstanceStatus', 'AutoMinorVersionUpgrade', 'DBInstanceClass', 'MultiAZ', 'Endpoint', 'BackupRetentionPeriod', 'PubliclyAccessible', 'StorageEncrypted', 'VpcSecurityGroups', 'DBSecurityGroups', 'DBParameterGroups']:
            # parameter_groups , security_groups, vpc_security_gropus
            dbi_info[key] = dbi[key] if key in dbi else None
        region_info['vpcs'][vpc_id]['instances'][dbi_info['name']] = dbi_info
