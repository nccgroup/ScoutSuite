#!/usr/bin/env python2

# Import opinel
from opinel.utils_s3 import *

# Import AWS Scout2 tools
from AWSScout2.utils import *
from AWSScout2.filters import *
from AWSScout2.findings import *

# Import third-party packages
import botocore.client


########################################
##### S3 functions
########################################

def analyze_s3_config(s3_info, aws_account_id, force_write):
    printInfo('Analyzing S3 data...')
    analyze_config(s3_finding_dictionary, s3_filter_dictionary, s3_info, 'S3', force_write)

def init_s3_permissions():
    permissions = {}
    permissions['read'] = False
    permissions['write'] = False
    permissions['read_acp'] = False
    permissions['write_acp'] = False
    return permissions

def set_s3_permissions(permissions, name):
    if name == 'READ' or name == 'FULL_CONTROL':
        permissions['read'] = True
    if name == 'WRITE' or name == 'FULL_CONTROL':
        permissions['write'] = True
    if name == 'READ_ACP' or name == 'FULL_CONTROL':
        permissions['read_acp'] = True
    if name == 'WRITE_ACP' or name == 'FULL_CONTROL':
        permissions['write_acp'] = True

def s3_group_to_string(uri):
    if uri == 'http://acs.amazonaws.com/groups/global/AuthenticatedUsers':
        return 'Authenticated users'
    elif uri == 'http://acs.amazonaws.com/groups/global/AllUsers':
        return 'Everyone'
    elif uri == 'http://acs.amazonaws.com/groups/s3/LogDelivery':
        return 'Log delivery'
    else:
        return uri

def get_s3_acls(s3_client, bucket_name, bucket, key_name = None):
  try:
    grantees = {}
    if key_name:
        grants = s3_client.get_object_acl(Bucket = bucket_name, Key = key_name)
    else:
        grants = s3_client.get_bucket_acl(Bucket = bucket_name)
    for grant in grants['Grants']:
        if 'ID' in grant['Grantee']:
            grantee = grant['Grantee']['ID']
            display_name = grant['Grantee']['DisplayName']
        elif 'URI' in grant['Grantee']:
            grantee = grant['Grantee']['URI']
            display_name = s3_group_to_string(grantee)
        else:
            grantee = display_name = 'Unknown'
        permission = grant['Permission']
        manage_dictionary(grantees, grantee, {})
        grantees[grantee]['DisplayName'] = display_name
        manage_dictionary(grantees[grantee], 'permissions', init_s3_permissions())
        set_s3_permissions(grantees[grantee]['permissions'], permission)
    if key_name:
        bucket['keys'][key_name]['grantees'] = grantees
    else:
        bucket['grantees'] = grantees
  except Exception as e:
    printException(e)

def get_s3_bucket_policy(s3_client, bucket_name, bucket_info):
    try:
        bucket_info['policy'] = json.loads(s3_client.get_bucket_policy(Bucket = bucket_name)['Policy'])
    except Exception as e:
        pass

def get_s3_bucket_versioning(s3_client, bucket_name, bucket_info):
    try:
        versioning = s3_client.get_bucket_versioning(Bucket = bucket_name)
        bucket_info['versioning_status'] = versioning['Status'] if 'Status' in versioning else 'Disabled'
        bucket_info['version_mfa_delete'] = versioning['MFADelete'] if 'MFADelete' in versioning else 'Disabled'
    except Exception as e:
        bucket_info['versioning_status'] = 'Unknown'
        bucket_info['version_mfa_delete'] = 'Unknown'

def get_s3_bucket_location(s3_client, bucket_name, bucket_info):
    location = s3_client.get_bucket_location(Bucket = bucket_name)
    bucket_info['region'] = location['LocationConstraint'] if location['LocationConstraint'] else 'us-east-1'

def get_s3_bucket_logging(s3_client, bucket_name, bucket_info):
    try:
        logging = s3_client.get_bucket_logging(Bucket = bucket_name)
        if 'LoggingEnabled' in logging:
            bucket_info['logging'] = logging['LoggingEnabled']['TargetBucket'] + '/' + logging['LoggingEnabled']['TargetPrefix']
            bucket_info['logging_stuff'] = logging
        else:
            bucket_info['logging'] = 'Disabled'
    except Exception as e:
        printError('Failed to get logging configuration for %s' % bucket_name)
        printException(e)
        bucket_info['logging'] = 'Unknown'

def get_s3_bucket_webhosting(s3_client, bucket_name, bucket_info):
    try:
        result = s3_client.get_bucket_website(Bucket = bucket_name)
        bucket_info['web_hosting'] = 'Enabled' if 'IndexDocument' in result else 'Disabled'
    except:
        pass

# List all available buckets
def get_s3_buckets(s3_client, s3_info, s3_params):
    manage_dictionary(s3_info, 'buckets', {})
    buckets = s3_client['us-east-1'].list_buckets()['Buckets']
    targets = []
    for b in buckets:
        # Abort if bucket is not of interest
        if (b['Name'] in s3_params['skipped_buckets']) or (len(s3_params['checked_buckets']) and b['Name'] not in s3_params['checked_buckets']):
            continue
        targets.append(b)
    s3_info['buckets_count'] = len(targets)
    thread_work(s3_client, s3_info, targets, get_s3_bucket, service_params = s3_params, num_threads = 30)
    show_status(s3_info)
    return s3_info

def get_s3_bucket(s3_clients, q, s3_params):
    while True:
        try:
            s3_info, bucket = q.get()
            s3_client = s3_clients['us-east-1']
            bucket['CreationDate'] = str(bucket['CreationDate'])
            get_s3_bucket_location(s3_client, bucket['Name'], bucket)
            # h4ck :: need to use the right endpoint because signature scheme autochange is not working
            s3_client = s3_clients[bucket['region']]
            get_s3_bucket_logging(s3_client, bucket['Name'], bucket)
            get_s3_bucket_versioning(s3_client, bucket['Name'], bucket)
            get_s3_bucket_webhosting(s3_client, bucket['Name'], bucket)
            get_s3_acls(s3_client, bucket['Name'], bucket)
            # TODO:
            # CORS
            # Lifecycle
            # Notification ?
            # Get bucket's policy
            get_s3_bucket_policy(s3_client, bucket['Name'], bucket)
            # If requested, get key properties
            if s3_params['check_encryption'] or s3_params['check_acls']:
                get_s3_bucket_keys(s3_client, bucket['Name'], bucket, s3_params['check_encryption'], s3_params['check_acls'])
            s3_info['buckets'][bucket['Name']] = bucket
            show_status(s3_info, False)
        except Exception as e:
            printError('Failed to get config for %s' % bucket['Name'])
            printException(e)
        finally:
            q.task_done()

# Get key-specific information (server-side encryption, acls, etc...)
def get_s3_bucket_keys(s3_client, bucket_name, bucket, check_encryption, check_acls):
    bucket['keys'] = {}
    keys = handle_truncated_responses(s3_client.list_objects, {'Bucket': bucket_name}, 'Contents')
    for key in keys:
        key_name = key.pop('Key')
        key['LastModified'] = str(key['LastModified'])
        bucket['keys'][key_name] = key
        if check_encryption:
            try:
                # The encryption configuration is only accessible via an HTTP header, only returned when requesting one object at a time...
                k = s3_client.get_object(Bucket = bucket_name, Key = key_name) # ['ServerSideEncryption']
                bucket['keys'][key_name]['ServerSideEncryption'] = k['ServerSideEncryption'] if 'ServerSideEncryption' in k else None
                bucket['keys'][key_name]['SSEKMSKeyId'] = k['SSEKMSKeyId'] if 'SSEKMSKeyId' in k else None
            except Exception as e:
                printException(e)
                continue
        if check_acls:
            try:
                get_s3_acls(s3_client, bucket_name, bucket, key_name = key_name)
            except Exception as e:
                continue

def get_s3_info(key_id, secret, session_token, service_config, selected_regions, fetch_gov, s3_params):
    # h4ck :: Create multiple clients here to avoid propagation of credentials. This is necessary because s3 is a global service that requires to access the API via the right region endpoints...
    s3_clients = {}
    for region in build_region_list('s3', selected_regions, include_gov = fetch_gov):
        config = botocore.client.Config(region_name = region, signature_version ='s3v4')
        s3_clients[region] = connect_s3(key_id, secret, session_token, region_name = region, config = config)
    printInfo('Fetching S3 buckets data...')
    get_s3_buckets(s3_clients, service_config, s3_params)

def show_status(s3_info, newline = True):
    current = len(s3_info['buckets'])
    total = s3_info['buckets_count']
    sys.stdout.write("\r%d/%d" % (current, total))
    sys.stdout.flush()
    if newline:
        sys.stdout.write('\n')
