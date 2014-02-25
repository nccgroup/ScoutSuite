#!/usr/bin/env python2

# Import the Amazon SDK
import boto

# Import other third-party packages
import copy
import json
import os
import sys
import traceback
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

class Scout2Encoder(json.JSONEncoder):
    def default(self, o):
        return o.__dict__


########################################
# Violations search functions
########################################

def analyze_config(finding_dictionary, config, keyword, force_write):
    try:
        for key in finding_dictionary:
            finding = finding_dictionary[key]
            entity_path = finding.entity.split('.')
            process_finding(config, finding)
        config['violations'] = finding_dictionary
    except:
        print 'Exception:\n %s' % traceback.format_exc()
        pass
    save_config_to_file(config, keyword, force_write)

def process_entities(config, finding, entity_path):
    if len(entity_path) == 1:
        entities = entity_path.pop(0)
        if entities in config:
            for key in config[entities]:
                finding.callback(finding, key, config[entities][key])
    elif len(entity_path) != 0:
        entities = entity_path.pop(0)
        for key in config[entities]:
            process_entities(config[entities][key], finding, copy.deepcopy(entity_path))
    else:
        print 'Unknown error'

def process_finding(config, finding):
    entity_path = finding.entity.split('.')
    process_entities(config, finding, entity_path)


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

def load_info_from_json(aws_service):
    filename = AWSCONFIG_DIR + '/' + aws_service + '_config.js'
    with open(filename) as f:
        json_payload = f.readlines()
        json_payload.pop(0)
#        json_payload.pop()
        json_payload = ''.join(json_payload)
        return json.loads(json_payload)

def load_findings(filename):
    with open(filename) as f:
        return json.load(f)

def load_from_json(keyword, var):
    filename = AWSCONFIG_DIR + '/' + keyword + '_config.js'
    with open(filename) as f:
        json_payload = f.readlines()
        json_payload.pop(0)
#        json_payload.pop()
        json_payload = ''.join(json_payload)
        return json.loads(json_payload)

def open_file(keyword, force_write):
    out_dir = AWSCONFIG_DIR
    print 'Saving ' + keyword + ' data...'
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    filename = out_dir + '/' + keyword.lower().replace(' ','_') + '_config.js'
    if not os.path.isfile(filename) or force_write:
        return open(filename, 'wt')
    else:
        print 'Error: ' + filename + ' already exists.'
        return None

def save_to_file(blob, keyword, force_write, columns_in_report=2, raw=True):
    with open_file(keyword, force_write) as f:
        keyword = write_data_to_file(f, blob, keyword, force_write, columns_in_report)

def save_config_to_file(blob, keyword, force_write):
    with open_file(keyword, force_write) as f:
        keyword = write_data_to_file(f, blob, keyword, force_write, 1)
#        print >>f, 'highlight_violations(%s_data);' % (keyword)

def write_data_to_file(f, blob, keyword, force_write, columns_in_report):
    keyword = keyword.lower().replace(' ','_') # [:-1]
    print >>f, keyword + '_info ='
    print >>f, '%s' % json.dumps(blob, indent=4, separators=(',', ': '), sort_keys=True, cls=Scout2Encoder)
#    print >>f, 'load_aws_config_from_json(%s_data, \'%s\', %d);' % (keyword, keyword, columns_in_report)
    return keyword


########################################
# Status update functions
########################################

def init_status(items, keyword=None):
    count = 0
    total = 0
    if items:
        total = len(items)
    update_status(0, total, keyword)
    return count, total

def update_status(current, total, keyword=None):
    if keyword:
        keyword = keyword + ':'
    else:
        keyword = ''
    if total != 0:
        sys.stdout.write("\r%s %d/%d" % (keyword , current, total))
    else:
        sys.stdout.write("\r%s %d" % (keyword, current))
    sys.stdout.flush()
    #lol TODO h4ck REMOVEME
    return current + 1

def close_status(current, total, keyword=None):
    update_status(current, total, keyword)
    sys.stdout.write('\n')
