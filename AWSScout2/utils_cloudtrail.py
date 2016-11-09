# Import opinel
from opinel.utils import *
from opinel.utils_cloudtrail import *

# Import Scout2 tools
from AWSScout2.utils import *

########################################
##### CloudTrails functions
########################################

def tweak_cloudtrail_findings(aws_config):
    cloudtrail_config = aws_config['services']['cloudtrail']
    # Global services logging duplicated
    if 'cloudtrail-duplicated-global-services-logging' in aws_config['services']['cloudtrail']['violations']:
        if len(aws_config['services']['cloudtrail']['violations']['cloudtrail-duplicated-global-services-logging']['items']) < 2:
            aws_config['services']['cloudtrail']['violations']['cloudtrail-duplicated-global-services-logging']['items'] = []
            aws_config['services']['cloudtrail']['violations']['cloudtrail-duplicated-global-services-logging']['flagged_items'] = 0
    # Global services logging disabled
    if 'cloudtrail-no-global-services-logging' in aws_config['services']['cloudtrail']['violations']:
        if len(aws_config['services']['cloudtrail']['violations']['cloudtrail-no-global-services-logging']['items']) != aws_config['services']['cloudtrail']['violations']['cloudtrail-no-global-services-logging']['checked_items']:
            aws_config['services']['cloudtrail']['violations']['cloudtrail-no-global-services-logging']['items'] = []
            aws_config['services']['cloudtrail']['violations']['cloudtrail-no-global-services-logging']['flagged_items'] = 0
    # CloudTrail not enabled at all...
    if not sum(aws_config['services']['cloudtrail']['regions'][r]['trails_count'] for r in aws_config['services']['cloudtrail']['regions']):
        for r in aws_config['services']['cloudtrail']['regions']:
            aws_config['services']['cloudtrail']['violations']['cloudtrail-no-logging']['items'].append('cloudtrail.regions.%s' % r)
            aws_config['services']['cloudtrail']['violations']['cloudtrail-no-logging']['checked_items'] += 1
            aws_config['services']['cloudtrail']['violations']['cloudtrail-no-logging']['flagged_items'] += 1
            aws_config['services']['cloudtrail']['violations']['cloudtrail-no-logging']['dashboard_name'] = 'Regions'

def get_cloudtrail_info(credentials, service_config, selected_regions, with_gov, with_cn):
    manage_dictionary(service_config, 'regions', {})
    printInfo('Fetching CloudTrail config...')
    for region in build_region_list('cloudtrail', selected_regions, include_gov = with_gov, include_cn = with_cn):
        manage_dictionary(service_config['regions'], region, {})
        service_config['regions'][region]['name'] = region
    thread_work(service_config['regions'], get_region_trails, params = {'creds': credentials, 'cloudtrail_info': service_config})
    service_config['regions_count'] = len(service_config['regions'])

def get_region_trails(q, params):
    cloudtrail_info = params['cloudtrail_info']
    while True:
      try:
        region = q.get()
        manage_dictionary(cloudtrail_info['regions'][region], 'trails', {})
        cloudtrail_client = connect_cloudtrail(params['creds'], region)
        trails = cloudtrail_client.describe_trails()
        cloudtrail_info['regions'][region]['trails_count'] = len(trails['trailList'])
        for trail in trails['trailList']:
            trail_info = {}
            trail_info['name'] = trail.pop('Name')
            # Do not duplicate entries for multiregion trails
            if 'IsMultiRegionTrail' in trail and trail['IsMultiRegionTrail'] and trail['HomeRegion'] != region:
                for key in ['HomeRegion', 'TrailARN']:
                    trail_info[key] = trail[key]
                trail_info['scout2_link'] = 'services.cloudtrail.regions.%s.trails.%s' % (trail['HomeRegion'], get_non_aws_id(trail_info['name']))
            else:
                for key in trail:
                    trail_info[key] = trail[key]
                trail_info['bucket_id'] = get_non_aws_id(trail_info.pop('S3BucketName'))
                for key in ['IsMultiRegionTrail', 'LogFileValidationEnabled']:
                    if key not in trail_info:
                        trail_info[key] = False
                trail_details = cloudtrail_client.get_trail_status(Name = trail['TrailARN'])
                for key in ['IsLogging', 'LatestDeliveryTime', 'LatestDeliveryError', 'StartLoggingTime', 'StopLoggingTime', 'LatestNotificationTime', 'LatestNotificationError', 'LatestCloudWatchLogsDeliveryError', 'LatestCloudWatchLogsDeliveryTime']:
                    trail_info[key] = trail_details[key] if key in trail_details else None
            cloudtrail_info['regions'][region]['trails'][get_non_aws_id(trail_info['name'])] = trail_info
      except Exception as e:
          printException(e)
      finally:
        q.task_done()

