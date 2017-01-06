# Import opinel
from opinel.utils import *

# Import Scout2 tools
from AWSScout2.utils import *


########################################
##### Globals
########################################

fetched_topics = 0
discovered_topics = 0


########################################
##### SNS functions
########################################

#
# Get SNS config in all regions in scope
#
def get_sns_info(credentials, service_config, selected_regions, partition_name):
    manage_dictionary(service_config, 'regions', {})
    printInfo('Fetching SNS config...')
    for region in build_region_list('sns', selected_regions, partition_name):
        manage_dictionary(service_config['regions'], region, {})
        service_config['regions'][region]['name'] = region        
    thread_work(service_config['regions'], threaded_per_region, params = {'method': get_sns_region, 'creds': credentials, 'sns_config': service_config})
    service_config['regions_count'] = len(service_config['regions'])
    status_update(True)


#
# Get SNS config in a single region
#
def get_sns_region(params):
    global fetched_topics
    region = params['region']
    sns_config = params['sns_config']
    manage_dictionary(sns_config['regions'][region], 'topics', {})
    sns_client = connect_service('sns', params['creds'], region)
    sns_config['regions'][region]['topics'] = {}
    topics = handle_truncated_response(sns_client.list_topics, {}, 'NextToken', ['Topics'])['Topics']
    sns_config['regions'][region]['topics_count'] = len(topics)
    update_cross_region_total(sns_config['regions'][region]['topics_count'])
    status_update()
    for topic in topics:
        topic['arn'] = topic.pop('TopicArn')
        attributes = sns_client.get_topic_attributes(TopicArn = topic['arn'])['Attributes']
        for k in ['Owner', 'DisplayName', 'SubscriptionsPending', 'SubscriptionsConfirmed', 'SubscriptionsDeleted']:
            topic[k] = attributes[k] if k in attributes else None
        for k in ['Policy', 'DeliveryPolicy', 'EffectiveDeliveryPolicy']:
            topic[k] = json.loads(attributes[k]) if k in attributes else None
        topic['name'] = topic['arn'].split(':')[-1]
        sns_config['regions'][region]['topics'][topic['name']] = topic
        fetched_topics += 1


########################################
##### Status display
########################################

def update_cross_region_total(region_count):
    global discovered_topics
    discovered_topics += region_count

def status_update(newline = False):
    global fetched_topics, discovered_topics
    sys.stdout.write('\r Topics: %d/%d' % (fetched_topics, discovered_topics))
    sys.stdout.flush()
    if newline:
        sys.stdout.write('\n')
