#!/usr/bin/env python2

# Import AWS Utils
from AWSUtils.utils_s3 import *

# Import AWS Scout2 tools
from AWSScout2.utils import *
from AWSScout2.filters import *
from AWSScout2.findings import *

# Import third-party packages
import boto


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
def get_s3_buckets(s3_connection, s3_info, s3_params):
    manage_dictionary(s3_info, 'buckets', {})
    buckets = s3_connection.get_all_buckets()
    targets = []
    for b in buckets:
        # Abort if bucket is not of interest
        if (b.name in s3_params['skipped_buckets']) or (len(s3_params['checked_buckets']) and b.name not in s3_params['checked_buckets']):
            continue
        targets.append(b)
    s3_info['buckets_count'] = len(targets)
    thread_work(s3_connection, s3_info, targets, get_s3_bucket, show_status_thread, service_params = s3_params, num_threads = 5)
    show_status(s3_info)
    return s3_info

def get_s3_bucket(s3_connection, q, s3_params):
    while True:
        try:
            s3_info, b = q.get()
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
            if s3_params['check_encryption'] or s3_params['check_acls']:
                get_s3_bucket_keys(b, bucket, s3_params['check_encryption'], s3_params['check_acls'])
            s3_info['buckets'][b.name] = bucket
        except Exception, e:
            printException(e)
        finally:
            q.task_done()

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

def get_s3_info(key_id, secret, session_token, s3_info, s3_params):
    s3_connection = connect_s3(key_id, secret, session_token)
    print 'Fetching S3 buckets data...'
    get_s3_buckets(s3_connection, s3_info, s3_params)
    return s3_info

def show_status_thread(s3_info, stop_event):
    while(not stop_event.is_set()):
        show_status(s3_info, False)
        stop_event.wait(1)

def show_status(s3_info, newline = True):
    sys.stdout.write("\r%d/%d" % (len(s3_info['buckets']), s3_info['buckets_count']))
    sys.stdout.flush()
    if newline:
        sys.stdout.write('\n')
