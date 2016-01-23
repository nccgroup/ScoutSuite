
# Import opinel
from opinel.utils_redshift import *

# Import AWS Scout2 tools
from AWSScout2.utils import *


########################################
##### Redshift fetching
########################################

#
# Entry point
#
def get_redshift_info(key_id, secret, session_token, service_config, selected_regions, with_gov, with_cn):
    printInfo('Fetching Redshift config...')
    manage_dictionary(service_config, 'regions', {}) 
    regions = build_region_list('redshift', selected_regions, include_gov = with_gov, include_cn = with_cn)
    for region in regions:
        manage_dictionary(service_config['regions'], region, {})
        manage_dictionary(service_config['regions'][region], 'vpcs', {})
    thread_work(service_config['regions'], get_redshift_region, params = {'creds': (key_id, secret, session_token), 'redshift_config': service_config})
    for region in regions:
       if len(service_config['regions'][region]['security_groups']):
           manage_dictionary(service_config['regions'][region]['vpcs'], ec2_classic, {})
           service_config['regions'][region]['vpcs'][ec2_classic]['security_groups'] = service_config['regions'][region].pop('security_groups')

#
# Region threading
#
def get_redshift_region(q, params):
    key_id, secret, session_token = params['creds']
    redshift_config = params['redshift_config']
    while True:
        try:
            region = q.get()
            redshift_client = connect_redshift(key_id, secret, session_token, region)
            get_redshift_clusters(redshift_client, redshift_config['regions'][region])
            get_redshift_cluster_parameter_groups(redshift_client, redshift_config['regions'][region])
            get_redshift_cluster_security_groups(redshift_client, redshift_config['regions'][region])
        except Exception as e:
            printException(e)
            pass
        finally:
            q.task_done()

#
# Clusters
#
def get_redshift_clusters(redshift_client, region_config):
    clusters = handle_truncated_response(redshift_client.describe_clusters, {}, 'Marker', ['Clusters'])
    for cluster in clusters['Clusters']:
        vpc_id = cluster.pop('VpcId') if 'VpcId' in cluster else ec2_classic
        manage_dictionary(region_config['vpcs'], vpc_id, {})
        manage_dictionary(region_config['vpcs'][vpc_id], 'clusters', {})
        name = cluster.pop('ClusterIdentifier')
        cluster['name'] = name
        region_config['vpcs'][vpc_id]['clusters'][name] = cluster

#
# Parameter groups
#
def get_redshift_cluster_parameter_groups(redshift_client, region_config):
    region_config['parameter_groups'] = {}
    parameter_groups = handle_truncated_response(redshift_client.describe_cluster_parameter_groups, {}, 'Marker', ['ParameterGroups'])
    for parameter_group in parameter_groups['ParameterGroups']:
        name = parameter_group.pop('ParameterGroupName')
        region_config['parameter_groups'][name] = parameter_group
        region_config['parameter_groups'][name]['name'] = name
        parameters = handle_truncated_response(redshift_client.describe_cluster_parameters, {'ParameterGroupName': name}, 'Marker', ['Parameters'])
        region_config['parameter_groups'][name]['parameters'] = {}
        for parameter in parameters['Parameters']:
            param = {}
            param['value'] = parameter['ParameterValue']
            param['source'] = parameter['Source']
            region_config['parameter_groups'][name]['parameters'][parameter['ParameterName']] = param

#
# Security groups
#
def get_redshift_cluster_security_groups(redshift_client, region_config):
    try:
        region_config['security_groups'] = {}
        security_groups = handle_truncated_response(redshift_client.describe_cluster_security_groups, {}, 'Marker', ['ClusterSecurityGroups'])
        for security_group in security_groups['ClusterSecurityGroups']:
            name = security_group.pop('ClusterSecurityGroupName')
            region_config['security_groups'][name] = security_group
            region_config['security_groups'][name]['name'] = name
    except Exception as e:
        # An exception occurs when VPC-by-default customers make this call, silently pass
        pass
