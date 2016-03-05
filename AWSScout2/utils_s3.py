
# Import opinel
from opinel.utils_s3 import *

# Import AWS Scout2 tools
from AWSScout2.utils import *

# Import third-party packages
import botocore.client

########################################
##### S3 functions
########################################

def match_iam_policies_and_buckets(s3_info, iam_info):
    if 'Action' in iam_info['permissions']:
        for action in (x for x in iam_info['permissions']['Action'] if ((x.startswith('s3:') and x != 's3:ListAllMyBuckets') or (x == '*'))):
            for iam_entity in iam_info['permissions']['Action'][action]:
                if 'Allow' in iam_info['permissions']['Action'][action][iam_entity]:
                    for allowed_iam_entity in iam_info['permissions']['Action'][action][iam_entity]['Allow']:
                        # For resource statements, we can easily rely on the existing permissions structure
                        if 'Resource' in iam_info['permissions']['Action'][action][iam_entity]['Allow'][allowed_iam_entity]:
                            for full_path in (x for x in iam_info['permissions']['Action'][action][iam_entity]['Allow'][allowed_iam_entity]['Resource'] if x.startswith('arn:aws:s3:') or x == '*'):
                                parts = full_path.split('/')
                                bucket_name = parts[0].split(':')[-1]
                                update_iam_permissions(s3_info, bucket_name, iam_entity, allowed_iam_entity, iam_info['permissions']['Action'][action][iam_entity]['Allow'][allowed_iam_entity]['Resource'][full_path])
                        # For notresource statements, we must fetch the policy document to determine which buckets are not protected
                        if 'NotResource' in iam_info['permissions']['Action'][action][iam_entity]['Allow'][allowed_iam_entity]:
                            for full_path in (x for x in iam_info['permissions']['Action'][action][iam_entity]['Allow'][allowed_iam_entity]['NotResource'] if x.startswith('arn:aws:s3:') or x == '*'):
                                for policy_type in ['InlinePolicies', 'ManagedPolicies']:
                                    if policy_type in iam_info['permissions']['Action'][action][iam_entity]['Allow'][allowed_iam_entity]['NotResource'][full_path]:
                                        for policy in iam_info['permissions']['Action'][action][iam_entity]['Allow'][allowed_iam_entity]['NotResource'][full_path][policy_type]:
                                            update_bucket_permissions(s3_info, iam_info, action, iam_entity, allowed_iam_entity, full_path, policy_type, policy)


def update_iam_permissions(s3_info, bucket_name, iam_entity, allowed_iam_entity, policy_info):
    if bucket_name != '*' and bucket_name in s3_info['buckets']:
        bucket = s3_info['buckets'][bucket_name]
        manage_dictionary(bucket, iam_entity, {})
        manage_dictionary(bucket, iam_entity + '_count', 0)
        if not allowed_iam_entity in bucket[iam_entity]:
            bucket[iam_entity][allowed_iam_entity] = {}
            bucket[iam_entity + '_count'] = bucket[iam_entity + '_count'] + 1

        if 'inline_policies' in policy_info:
            manage_dictionary(bucket[iam_entity][allowed_iam_entity], 'inline_policies', {})
            bucket[iam_entity][allowed_iam_entity]['inline_policies'].update(policy_info['inline_policies'])
        if 'managed_policies' in policy_info:
            manage_dictionary(bucket[iam_entity][allowed_iam_entity], 'managed_policies', {})
            bucket[iam_entity][allowed_iam_entity]['managed_policies'].update(policy_info['managed_policies'])
    elif bucket_name == '*':
        for bucket in s3_info['buckets']:
            update_iam_permissions(s3_info, bucket, iam_entity, allowed_iam_entity, policy_info)
        pass
    else:
        # Could be an error or cross-account access, ignore...
        pass

def update_bucket_permissions(s3_info, iam_info, action, iam_entity, allowed_iam_entity, full_path, policy_type, policy_name):
    allowed_buckets = []
    # By default, all buckets are allowed
    for bucket_name in s3_info['buckets']:
        allowed_buckets.append(bucket_name)
    if policy_type == 'InlinePolicies':
        policy = iam_info[iam_entity.title()][allowed_iam_entity]['Policies'][policy_name]['PolicyDocument']
    elif policy_type == 'ManagedPolicies':
        policy = iam_info['ManagedPolicies'][policy_name]['PolicyDocument']
    else:
        printError('Error, found unknown policy type.')
    for statement in policy['Statement']:
        for target_path in statement['NotResource']:
            parts = target_path.split('/')
            bucket_name = parts[0].split(':')[-1]
            path = '/' + '/'.join(parts[1:]) if len(parts) > 1 else '/'
            if (path == '/' or path == '/*') and (bucket_name in allowed_buckets):
                # Remove bucket from list
                allowed_buckets.remove(bucket_name)
            elif bucket_name == '*':
                allowed_buckets = []
    policy_info = {}
    policy_info[policy_type] = {}
    policy_info[policy_type][policy_name] = iam_info['permissions']['Action'][action][iam_entity]['Allow'][allowed_iam_entity]['NotResource'][full_path][policy_type][policy_name]
    for bucket_name in allowed_buckets:
        update_iam_permissions(s3_info, bucket_name, iam_entity, allowed_iam_entity, policy_info)

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
            display_name = grant['Grantee']['DisplayName'] if 'DisplayName' in grant['Grantee'] else grant['Grantee']['ID']
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
    return grantees
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
    except Exception as e:
        # TODO: distinguish permission denied from  'NoSuchWebsiteConfiguration' errors
        bucket_info['web_hosting'] = 'Disabled'
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
    s3_params['s3_clients'] = s3_client
    s3_params['s3_info'] = s3_info
    thread_work(targets, get_s3_bucket, params = s3_params, num_threads = 30)
    show_status(s3_info)
    s3_info['buckets_count'] = len(s3_info['buckets'])
    return s3_info

def get_s3_bucket(q, params):
    s3_clients = params['s3_clients']
    s3_info = params['s3_info']
    while True:
        try:
            bucket = q.get()
            bucket['name'] = bucket.pop('Name')
            s3_client = s3_clients['us-east-1']
            bucket['CreationDate'] = str(bucket['CreationDate'])
            bucket['region'] = get_s3_bucket_location(s3_client, bucket['name'])
            # h4ck :: fix issue #59, location constraint can be EU or eu-west-1 for Ireland...
            if bucket['region'] == 'EU':
                bucket['region'] = 'eu-west-1'
            # h4ck :: S3 is global but region-aware... 
            if params['selected_regions'] != [] and bucket['region'] not in params['selected_regions']:
                printInfo('Skipping bucket %s (region %s outside of scope)' % (bucket['name'], bucket['region']))
                s3_info['buckets_count'] = s3_info['buckets_count'] - 1
            else:
                # h4ck :: need to use the right endpoint because signature scheme autochange is not working
                s3_client = s3_clients[bucket['region']]
                get_s3_bucket_logging(s3_client, bucket['name'], bucket)
                get_s3_bucket_versioning(s3_client, bucket['name'], bucket)
                get_s3_bucket_webhosting(s3_client, bucket['name'], bucket)
                bucket['grantees'] = get_s3_acls(s3_client, bucket['name'], bucket)
                # TODO:
                # CORS
                # Lifecycle
                # Notification ?
                # Get bucket's policy
                get_s3_bucket_policy(s3_client, bucket['name'], bucket)
                # If requested, get key properties
                if params['check_encryption'] or params['check_acls']:
                    get_s3_bucket_keys(s3_client, bucket['name'], bucket, params['check_encryption'], params['check_acls'])
                # h4ck :: buckets may contain . in their name, but this would break the browsing - Use sha1(bucket_name) as keys for the dictionary
                bucket['id'] = get_non_aws_id(bucket['name'])
                s3_info['buckets'][bucket['id']] = bucket
            show_status(s3_info, False)
        except Exception as e:
            printError('Failed to get config for %s' % bucket['name'])
            printException(e)
        finally:
            q.task_done()

# Get key-specific information (server-side encryption, acls, etc...)
def get_s3_bucket_keys(s3_client, bucket_name, bucket, check_encryption, check_acls):
    bucket['keys'] = []
    keys = handle_truncated_response(s3_client.list_objects, {'Bucket': bucket_name}, 'Marker', ['Contents'])
    bucket['keys_count'] = len(keys['Contents'])
    key_count = 0
    update_status(key_count, bucket['keys_count'], 'keys')
    for key in keys['Contents']:
        key_count += 1
        key['name'] = key.pop('Key')
        key['LastModified'] = str(key['LastModified'])
        if check_encryption:
            try:
                # The encryption configuration is only accessible via an HTTP header, only returned when requesting one object at a time...
                k = s3_client.get_object(Bucket = bucket_name, Key = key['name'])
                key['ServerSideEncryption'] = k['ServerSideEncryption'] if 'ServerSideEncryption' in k else None
                key['SSEKMSKeyId'] = k['SSEKMSKeyId'] if 'SSEKMSKeyId' in k else None
            except Exception as e:
                printException(e)
                continue
        if check_acls:
            try:
                key['grantees'] = get_s3_acls(s3_client, bucket_name, bucket, key_name = key['name'])
            except Exception as e:
                continue
        # Save it
        bucket['keys'].append(key)
        update_status(key_count, bucket['keys_count'], 'keys')


def get_s3_info(key_id, secret, session_token, service_config, selected_regions, with_gov, with_cn, s3_params):
    # h4ck :: Create multiple clients here to avoid propagation of credentials. This is necessary because s3 is a global service that requires to access the API via the right region endpoints...
    s3_clients = {}
    if selected_regions != []:
        client_regions = copy.deepcopy(selected_regions)
        client_regions.append('us-east-1')
    else:
        client_regions = selected_regions
    for region in build_region_list('s3', client_regions, include_gov = with_gov, include_cn = with_cn):
        config = botocore.client.Config(signature_version = 's3v4')
        s3_clients[region] = connect_s3(key_id, secret, session_token, region_name = region, config = config)
    s3_params['selected_regions'] = selected_regions
    printInfo('Fetching S3 buckets config...')
    get_s3_buckets(s3_clients, service_config, s3_params)

def show_status(s3_info, newline = True):
    current = len(s3_info['buckets'])
    total = s3_info['buckets_count']
    sys.stdout.write("\r%d/%d" % (current, total))
    sys.stdout.flush()
    if newline:
        sys.stdout.write('\n')
