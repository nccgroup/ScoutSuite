
# Import opinel
from opinel.utils_redshift import *

# Import AWS Scout2 tools
from AWSScout2.utils import *
from AWSScout2.filters import *
from AWSScout2.findings import *

########################################
# Globals
########################################
supported_services.append('redshift')

########################################
##### Redshift analysis
########################################

# Analysis
def analyze_redshift_config(redshift_config, aws_account_id, force_write):
    printInfo('Analyzing Redshift config...')
    analyze_config(redshift_finding_dictionary, redshift_filter_dictionary, redshift_config, 'Redshift')

########################################
##### Redshift fetching
########################################

#
# Entry point
#
def get_redshift_info(key_id, secret, session_token, service_config, selected_regions, with_gov, with_cn):
    manage_dictionary(service_config, 'regions', {})
    for region in build_region_list('redshift', selected_regions, include_gov = with_gov, include_cn = with_cn):
        manage_dictionary(service_config['regions'], region, {})
    thread_work(service_config['regions'], get_redshift_region, params = {'creds': (key_id, secret, session_token), 'redshift_config': service_config})

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
    region_config['clusters'] = {}
    clusters = handle_truncated_response(redshift_client.describe_clusters, {}, ['Clusters'])
    for cluster in clusters['Clusters']:
        cluster_id = cluster.pop('ClusterIdentifier')
        region_config['clusters'][cluster_id] = cluster

#
# Parameter groups
#
def get_redshift_cluster_parameter_groups(redshift_client, region_config):
    region_config['parameter_groups'] = {}
    parameter_groups = handle_truncated_response(redshift_client.describe_cluster_parameter_groups, {}, ['ParameterGroups'])
    for parameter_group in parameter_groups['ParameterGroups']:
        parameter_group_name = parameter_group.pop('ParameterGroupName')
        region_config['parameter_groups'][parameter_group_name] = parameter_group
        parameters = handle_truncated_response(redshift_client.describe_cluster_parameters, {'ParameterGroupName': parameter_group_name}, ['Parameters'])
        region_config['parameter_groups'][parameter_group_name]['parameters'] = []
        for parameter in parameters['Parameters']:
            param = {}
            for key in ['ParameterName', 'ParameterValue', 'Source']:
                param[key] = parameter[key]
            region_config['parameter_groups'][parameter_group_name]['parameters'].append(param)

#
# Security groups
#
def get_redshift_cluster_security_groups(redshift_client, region_config):
    try:
        region_config['security_groups'] = {}
        csgs = handle_truncated_response(redshift_client.describe_cluster_security_groups, {}, ['ClusterSecurityGroups'])
        region_config['security_groups'] = csgs['ClusterSecurityGroups']
    except Exception as e:
        # An exception occurs when VPC-by-default customers make this call, silently pass
        pass
