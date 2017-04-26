# Import opinel
from opinel.utils import *

# Import Scout2 tools
from AWSScout2.utils import *


########################################
##### Globals
########################################

fetched_alarms = 0
discovered_alarms = 0
fetched_metrics = 0
discovered_metrics = 0


########################################
##### CloudWatch functions
########################################

#
# Get CloudWatch config in all regions in scope
#
def get_cloudwatch_info(credentials, service_config, selected_regions, partition_name):
    manage_dictionary(service_config, 'regions', {})
    printInfo('Fetching CloudWatch config...')
    cloudwatch_status_init()
    for region in build_region_list('cloudwatch', selected_regions, partition_name):
        manage_dictionary(service_config['regions'], region, {})
        service_config['regions'][region]['name'] = region
    thread_work(service_config['regions'], threaded_per_region, params = {'method': get_cloudwatch_region, 'creds': credentials, 'cloudwatch_config': service_config})
    service_config['regions_count'] = len(service_config['regions'])
    cloudwatch_status(True)


#
# Get CloudWatch config in a single region
#
def get_cloudwatch_region(params):
    global fetched_alarms, discovered_alarms, fetched_metrics, discovered_metrics
    region = params['region']
    cloudwatch_config = params['cloudwatch_config']
    manage_dictionary(cloudwatch_config['regions'][region], 'metrics', {})
    cloudwatch_client = connect_service('cloudwatch', params['creds'], region)
    metrics = {}
    cloudwatch_config['regions'][region]['alarms'] = {}
    alarms = handle_truncated_response(cloudwatch_client.describe_alarms, {}, ['MetricAlarms'])['MetricAlarms']
    cloudwatch_config['regions'][region]['alarms_count'] = len(alarms)
    discovered_alarms += len(alarms)
    cloudwatch_status()
    for alarm in alarms:
        alarm['arn'] = alarm.pop('AlarmArn')
        alarm['name'] = alarm.pop('AlarmName')
        # Drop some data 
        for k in ['AlarmConfigurationUpdatedTimestamp', 'StateReason', 'StateReasonData', 'Statistic', 'ComparisonOperator', 'Threshold', 'StateUpdatedTimestamp']:
            foo = alarm.pop(k) if k in alarm else None
        alarm_id = get_non_aws_id(alarm['arn'])
        metric_id = get_non_aws_id('%s/%s' % (alarm['Namespace'], alarm['MetricName']))
        cloudwatch_config['regions'][region]['alarms'][alarm_id] = alarm
        manage_dictionary(metrics, metric_id, {'name': alarm['MetricName'],        'namespace': alarm['Namespace']})
        fetched_alarms += 1
        cloudwatch_status()
    cloudwatch_config['regions'][region]['alarms'] = alarms
    cloudwatch_config['regions'][region]['metrics'] = metrics
    cloudwatch_config['regions'][region]['metrics_count'] = len(metrics)
    #printInfo('Fetching metrics in %s...' % region)
    #metrics = handle_truncated_response(cloudwatch_client.list_metrics, {}, ['Metrics'])['Metrics']
    #for metric in metrics:
    #cloudwatch_config['regions'][region]['metrics_count'] = len(metrics)
    #cloudwatch_config['regions'][region]['metrics'] = metrics