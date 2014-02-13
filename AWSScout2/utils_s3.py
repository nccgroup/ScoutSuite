#!/usr/bin/env python2

# Import AWS Scout2 tools
from AWSScout2.utils import *
from AWSScout2.findings_s3 import *


########################################
##### S3 functions
########################################

def analyze_s3_config(buckets, force_write):
    print 'Analyzing S3 data...'
    s3_config = {"buckets": buckets}
    analyze_config_new(s3_finding_dictionary, s3_config, 'S3 violations', force_write)

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

# List all available buckets
def get_s3_buckets(s3):
    s3_buckets = {}
    buckets = s3.get_all_buckets()
    count, total = init_status(buckets)
    for b in buckets:
        count = update_status(count, total)
        bucket = {}
        acp = b.get_acl()
        bucket['grants'] = {}
        for grant in acp.acl.grants:
            grantee_name = 'Unknown'
            if grant.type == 'Group':
                grantee_name = s3_group_to_string(grant.uri)
                grant.uri.rsplit('/',1)[0]
            elif grant.type == 'CanonicalUser':
                grantee_name = grant.display_name
            manage_dictionary(bucket['grants'], grantee_name, {}, init_s3_permissions)
            set_s3_permission(bucket['grants'][grantee_name], grant.permission)
            bucket['grants'][grantee_name]['email'] = grant.email_address
        bucket['creation_date'] = b.creation_date
        bucket['region'] = b.get_location()
        bucket['logging'] = get_s3_bucket_logging(b)
        bucket['versioning'] = get_s3_bucket_versioning(b)
        s3_buckets[b.name] = bucket
    close_status(count, total)
    return s3_buckets
