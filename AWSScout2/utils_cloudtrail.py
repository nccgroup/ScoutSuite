#!/usr/bin/env python2

# Import the Amazon SDK
from boto import cloudtrail

# Import AWS Scout2 tools
from utils import *
from findings import *


########################################
##### CloudTrails functions
########################################

def analyze_cloudtrail_config(cloudtrail_info, force_write):
    analyze_config(cloudtrail_finding_dictionary, cloudtrail_info, 'CloudTrail', force_write)

def get_cloudtrail_info(key_id, secret, session_token):
    cloudtrail_info = {}
    cloudtrail_info['regions'] = {}
    for region in cloudtrail.regions():
        print 'Fetching CloudTrail data for region %s...' % region.name
        manage_dictionary(cloudtrail_info['regions'], region.name, {})
        cloudtrail_info['regions'][region.name]['name'] = region.name
        manage_dictionary(cloudtrail_info['regions'][region.name], 'trails', {})
        cloudtrail_connection = cloudtrail.connect_to_region(region.name, aws_access_key_id = key_id, aws_secret_access_key = secret, security_token = session_token)
        trails = cloudtrail_connection.describe_trails()
        count, total = init_status(None, 'CloudTrails')
        for trail in trails['trailList']:
            trail_info = {}
            for key in trail:
                trail_info[key] = trail[key]
            trail_details = cloudtrail_connection.get_trail_status(trail['Name'])
            for key in ['IsLogging', 'LatestDeliveryTime', 'StartLoggingTime', 'LatestNotificationError', 'LatestDeliveryError', 'LatestDeliveryAttemptSucceeded', 'LatestNotificationAttemptSucceeded']:
                trail_info[key] = trail_details[key] if key in trail_details else None
                trail_info['StopLoggingTime'] = trail_details['StopLoggingTime'] if  'StopLoggingTime' in trail_details else trail_details['TimeLoggingStopped']
                trail_info['LatestNotificationTime'] = trail_details['LatestNotificationTime'] if 'LatestNotificationTime' in trail_details else trail_details['LatestNotificationAttemptTime']
            cloudtrail_info['regions'][region.name]['trails'][trail['Name']] = trail_info
            count = update_status(count, total, 'CloudTrails')
        close_status(count, total, 'CloudTrails')
    return cloudtrail_info
