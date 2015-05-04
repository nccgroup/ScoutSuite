#!/usr/bin/env python2

# Import AWS Utils
from AWSUtils.utils import *
from AWSUtils.utils_cloudtrail import *

# Import Scout2 tools
from AWSScout2.utils import *
from AWSScout2.filters import *
from AWSScout2.findings import *

# Import third-party packages
import boto
from boto import cloudtrail

########################################
##### CloudTrails functions
########################################

def analyze_cloudtrail_config(cloudtrail_info, force_write):
    analyze_config(cloudtrail_finding_dictionary, cloudtrail_filter_dictionary, cloudtrail_info, 'CloudTrail', force_write)

def get_cloudtrail_info(profile_name):
    cloudtrail_info = {}
    cloudtrail_info['regions'] = {}
    for region in cloudtrail.regions():
        print 'Fetching CloudTrail data for region %s...' % region.name
        manage_dictionary(cloudtrail_info['regions'], region.name, {})
        cloudtrail_info['regions'][region.name]['name'] = region.name
        manage_dictionary(cloudtrail_info['regions'][region.name], 'trails', {})
        cloudtrail_connection = connect_cloudtrail(profile_name, region.name)
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
