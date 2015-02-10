#!/usr/bin/env python2

# Import the Amazon SDK
import boto

# Import AWS Scout2 tools
from AWSScout2.utils import *
from AWSScout2.filters import *
from AWSScout2.findings import *

########################################
##### S3 functions
########################################

def analyze_s3_config(s3_info, force_write):
    print 'Analyzing S3 data...'
    analyze_config(s3_finding_dictionary, s3_filter_dictionary, s3_info, 'S3', force_write)

def init_s3_permissions(grant):
    grant['read'] = False
    grant['write'] = False
    grant['read_acp'] = False
    grant['write_acp'] = False
    return grant

def set_s3_permission(grant, name):
    if name == 'READ' or name == 'FULL_CONTROL':
        grant['read'] = True
    if name == 'WRITE' or name == 'FULL_CONTROL':
        grant['write'] = True
    if name == 'READ_ACP' or name == 'FULL_CONTROL':
        grant['read_acp'] = True
    if name == 'WRITE_ACP' or name == 'FULL_CONTROL':
        grant['write_acp'] = True

def s3_group_to_string(uri):
    if uri == 'http://acs.amazonaws.com/groups/global/AuthenticatedUsers':
        return 'Authenticated users'
    elif uri == 'http://acs.amazonaws.com/groups/global/AllUsers':
        return 'All users'
    elif uri == 'http://acs.amazonaws.com/groups/s3/LogDelivery':
        return 'Log delivery'
    else:
        return uri

def get_s3_acls(bucket, key_name = None):
    grants = {}
    if key_name:
        acp = bucket.get_acl(key_name)
    else:
        acp = bucket.get_acl()
    for grant in acp.acl.grants:
        grantee_name = 'Unknown'
        if grant.type == 'Group':
            grantee_name = s3_group_to_string(grant.uri)
            grant.uri.rsplit('/',1)[0]
        elif grant.type == 'CanonicalUser':
            grantee_name = grant.display_name
        manage_dictionary(grants, grantee_name, {}, init_s3_permissions)
        set_s3_permission(grants[grantee_name], grant.permission)
        # h4ck : data redundancy because I can't call ../@key in Handlebars
        grants[grantee_name]['name'] = grantee_name
    return grants

def get_s3_bucket_versioning(bucket):
    r = bucket.get_versioning_status()
    if 'Versioning' in r:
        return r['Versioning']
    else:
        return 'Disabled'

def get_s3_bucket_logging(bucket):
    r = bucket.get_logging_status()
    if r.target is not None:
        return r.target + '/' + r.prefix
    else:
        return 'Disabled'

def get_s3_bucket_webhosting(bucket):
    try:
        if bucket.get_website_configuration():
            return 'Enabled'
    except:
        pass
    return 'Disabled'

# List all available buckets
def get_s3_buckets(s3_connection, s3_info, check_encryption, check_acls, checked_buckets, skipped_buckets):
    manage_dictionary(s3_info, 'buckets', {})
    buckets = s3_connection.get_all_buckets()
    count, total = init_status(buckets)
    for b in buckets:
        try:
            # Abort if bucket is not of interest
            if (b.name in skipped_buckets) or (len(checked_buckets) and b.name not in checked_buckets):
                continue
            # Get general bucket configuration
            bucket = {}
            bucket['grants'] = get_s3_acls(b)
            bucket['creation_date'] = b.creation_date
            bucket['region'] = b.get_location()
            bucket['logging'] = get_s3_bucket_logging(b)
            bucket['versioning'] = get_s3_bucket_versioning(b)
            bucket['web_hosting'] = get_s3_bucket_webhosting(b)
            # Get bucket's policy
            try:
                bucket['policy'] = b.get_policy()
            except Exception, e:
                # The bucket policy does not exist
                pass
            # h4ck : data redundancy because I can't call ../@key in Handlebars
            bucket['name'] = b.name
            # If requested, get key properties
            if check_encryption or check_acls:
                get_s3_bucket_keys(b, bucket, check_encryption, check_acls)
            s3_info['buckets'][b.name] = bucket
            count = update_status(count, total)
        except Exception, e:
            print e
    close_status(count, total)

# Get key-specific information (server-side encryption, acls, etc...)
def get_s3_bucket_keys(b, bucket, check_encryption, check_acls):
    bucket['keys'] = {}
    keys = b.list()
    for k in keys:
        manage_dictionary(bucket['keys'], k.name, {})
        try:
            if check_encryption:
                # The encryption configuration is only accessible via an HTTP header, only returned when requesting one object at a time...
                k = b.get_key(k.name)
                bucket['keys'][k.name]['encrypted'] = k.encrypted
                bucket['keys'][k.name]['storage_class'] = k.storage_class
            if check_acls:
                bucket['keys'][k.name]['grants'] = get_s3_acls(b, k.name)
        except Exception, e:
            continue

def get_s3_info(key_id, secret, session_token, s3_info, check_encryption, check_acls, checked_buckets, skipped_buckets):
    s3_connection = boto.connect_s3(aws_access_key_id = key_id, aws_secret_access_key = secret, security_token = session_token)
    print 'Fetching S3 buckets data...'
    get_s3_buckets(s3_connection, s3_info, check_encryption, check_acls, checked_buckets, skipped_buckets)
    return s3_info
