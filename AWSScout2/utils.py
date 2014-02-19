#!/usr/bin/env python2

# Import the Amazon SDK
import boto

# Import other third-party packages
import json
import os
import sys
import urllib2


########################################
# Common functions
########################################

def manage_dictionary(dictionary, key, init, callback=None):
    if not str(key) in dictionary:
        dictionary[str(key)] = init
        manage_dictionary(dictionary, key, init)
        if callback:
            callback(dictionary[key])
    return dictionary


########################################
# Violations search functions
########################################

def analyze_config(finding_dictionary, config, keyword, force_write):
    for key in finding_dictionary:
        finding = finding_dictionary[key]
        entity_path = finding.entity.split('.')
        entity_depth = len(entity_path)
        iterate_through_dictionary(config[entity_path[-1] + 's'], finding, None, entity_depth)
    save_violations_to_file(finding_dictionary.to_JSON(), keyword, force_write)

def iterate_through_dictionary(dictionary, finding, key, depth):
    if depth == 0:
        finding.callback(finding, key, dictionary)
    else:
        for key in dictionary:
            iterate_through_dictionary(dictionary[key], finding, key, depth -1)


########################################
# AWS Credentials read functions
########################################

def fetch_creds_from_instance_metadata():
    base_url = 'http://169.254.169.254/latest/meta-data/iam/security-credentials'
    try:
        iam_role = urllib2.urlopen(base_url).read()
        credentials = json.loads(urllib2.urlopen(base_url + '/' + iam_role).read())
        return credentials['AccessKeyId'], credentials['SecretAccessKey']
    except Exception, e:
        print 'Failed to fetch credentials. Make sure that this EC2 instance has an IAM role (%s)' % e
        return None, None

def fetch_creds_from_csv(filename):
    key_id = None
    secret = None
    with open(filename, 'rt') as csvfile:
        for i, line in enumerate(csvfile):
            if i == 1:
                username, key_id, secret = line.split(',')
    return key_id.rstrip(), secret.rstrip()

def fetch_sts_credentials(key_id, secret, mfa_serial, mfa_code):
    if not mfa_serial or len(mfa_serial) < 1:
        print 'Error, you need to provide your MFA device\'s serial number.'
        return None, None, None
    if not mfa_code or len(mfa_code) < 1:
        print 'Error, you need to provide the code displayed by your MFA device.'
        return None, None, None
    sts_connection = boto.connect_sts(key_id, secret)
    # For now, don't set the duration and use default 12hours
    sts_response = sts_connection.get_session_token(mfa_serial_number = mfa_serial[0], mfa_token = mfa_code[0])
    return sts_response.access_key, sts_response.secret_key, sts_response.session_token


########################################
# File read/write functions
########################################

AWSCONFIG_DIR = 'inc-awsconfig'

def load_findings(filename):
    with open(filename) as f:
        return json.load(f)

def load_from_json(keyword, var):
    filename = AWSCONFIG_DIR + '/aws_' + keyword + '_' + var + '.js'
    with open(filename) as f:
        json_payload = f.readlines()
        json_payload.pop(0)
        json_payload.pop()
        json_payload = ''.join(json_payload)
        return json.loads(json_payload)

def open_file(keyword, force_write):
    out_dir = AWSCONFIG_DIR
    print 'Saving ' + keyword + ' data...'
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    filename = out_dir + '/aws_' + keyword.lower().replace(' ','_') + '.js'
    if not os.path.isfile(filename) or force_write:
        return open(filename, 'wt')
    else:
        print 'Error: ' + filename + ' already exists.'
        return None

def save_to_file(blob, keyword, force_write, columns_in_report=2, raw=True):
    with open_file(keyword, force_write) as f:
        keyword = write_data_to_file(f, blob, keyword, force_write, columns_in_report, raw)

def save_violations_to_file(json_blob, keyword, force_write):
    with open_file(keyword, force_write) as f:
        keyword = write_data_to_file(f, json_blob, keyword, force_write, 1, False)
        print >>f, 'highlight_violations(%s_data);' % (keyword)

def write_data_to_file(f, blob, keyword, force_write, columns_in_report, raw):
    keyword = keyword.lower().replace(' ','_')[:-1]
    print >>f, keyword + '_data ='
    print >>f, '%s' % json.dumps(blob, indent=4, separators=(',', ': '), sort_keys=True) if raw else blob
    print >>f, 'load_aws_config_from_json(%s_data, \'%s\', %d);' % (keyword, keyword, columns_in_report)
    return keyword


########################################
# Status update functions
########################################

def init_status(items):
    if items:
        return 0, len(items)
    else:
        return 0, None

def update_status(current, total):
    current = current + 1
    if total:
        sys.stdout.write("\r %d/%d" % (current, total))
    else:
        sys.stdout.write("\r %d" % current)
    sys.stdout.flush()
    return current

def close_status(current, total):
    if current != 0:
        sys.stdout.write('\n')
