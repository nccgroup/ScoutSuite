# Import opinel
from opinel.utils import *

# Import Scout2 tools
from AWSScout2.utils import *


########################################
##### Globals
########################################

fetched_topics = 0
discovered_topics = 0
fetched_subscriptions = 0
discovered_subscriptions = 0


########################################
##### SNS functions
########################################

#
# Get SNS config in all regions in scope
#
def get_sns_info(credentials, service_config, selected_regions, partition_name):
    manage_dictionary(service_config, 'regions', {})
    printInfo('Fetching SNS config...')
    sns_status_init()
    for region in build_region_list('sns', selected_regions, partition_name):
        manage_dictionary(service_config['regions'], region, {})
        service_config['regions'][region]['name'] = region        
    thread_work(service_config['regions'], threaded_per_region, params = {'method': get_sns_region, 'creds': credentials, 'sns_config': service_config})
    service_config['regions_count'] = len(service_config['regions'])
    sns_status(True)


#
# Get SNS config in a single region
#
def get_sns_region(params):
    global fetched_topics, discovered_topics, fetched_subscriptions, discovered_subscriptions
    region = params['region']
    sns_config = params['sns_config']
    manage_dictionary(sns_config['regions'][region], 'topics', {})
    sns_client = connect_service('sns', params['creds'], region)
    # Get topics
    sns_config['regions'][region]['topics'] = {}
    topics = handle_truncated_response(sns_client.list_topics, {}, 'NextToken', ['Topics'])['Topics']
    sns_config['regions'][region]['topics_count'] = len(topics)
    discovered_topics += len(topics)
    sns_status()
    for topic in topics:
        topic['arn'] = topic.pop('TopicArn')
        attributes = sns_client.get_topic_attributes(TopicArn = topic['arn'])['Attributes']
        for k in ['Owner', 'DisplayName']:
            topic[k] = attributes[k] if k in attributes else None
        for k in ['Policy', 'DeliveryPolicy', 'EffectiveDeliveryPolicy']:
            topic[k] = json.loads(attributes[k]) if k in attributes else None
        topic['name'] = topic['arn'].split(':')[-1]
        manage_dictionary(topic, 'subscriptions', {})
        manage_dictionary(topic, 'subscriptions_count', 0)
        sns_config['regions'][region]['topics'][topic['name']] = topic
        fetched_topics += 1
        sns_status()
    # Get subscriptions and discard those for external topics
    subscriptions = handle_truncated_response(sns_client.list_subscriptions, {}, 'NextToken', ['Subscriptions'])['Subscriptions']
    discovered_subscriptions += len(subscriptions)
    sns_status()
    for s in subscriptions:
        topic_arn = s.pop('TopicArn')
        topic_name = topic_arn.split(':')[-1]
        if topic_name in sns_config['regions'][region]['topics']:
            topic = sns_config['regions'][region]['topics'][topic_name]
            manage_dictionary(topic['subscriptions'], 'protocol', {})
            protocol = s.pop('Protocol')
            manage_dictionary(topic['subscriptions']['protocol'], protocol, [])
            topic['subscriptions']['protocol'][protocol].append(s)
            topic['subscriptions_count'] += 1
        fetched_subscriptions += 1
        sns_status()


########################################
##### Status display
########################################

def sns_status_init():
    formatted_status('Topics', 'Subscriptions', True)

def sns_status(newline = False):
    global fetched_topics, discovered_topics, fetched_subscriptions, discovered_subscriptions
    a = '%d/%d' % (fetched_topics, discovered_topics)
    b = '%d/%d' % (fetched_subscriptions, discovered_subscriptions)
    formatted_status(a, b, newline)

def formatted_status(a, b, newline):
    sys.stdout.write('\r {:>15} {:>15}'.format(a, b))
    sys.stdout.flush()
    if newline:
        sys.stdout.write('\n')
