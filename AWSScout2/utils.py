#!/usr/bin/env python2

# Import the Amazon SDK
import boto
import boto.ec2

# Import other third-party packages
import json
import os
import sys
import urllib2


########################################
##### Common functions
########################################

def analyze_config(finding_dictionary, config, keyword, force_write):
    for finding in finding_dictionary['violations']:
        for entity in config[finding.entity + 's']:
            finding.callback(finding, entity)
    save_json_to_file(finding_dictionary.to_JSON(), keyword, force_write)

# Temporaryly create a _new function
# TODO modify the data structure of all other components to be dictionaries
def analyze_config_new(finding_dictionary, config, keyword, force_write):
    for finding in finding_dictionary['violations']:
        entity_path = finding.entity.split('.')
        entity_depth = len(entity_path)
        iterate_through_dictionary(config[entity_path[-1] + 's'], finding, None, entity_depth)
    save_json_to_file(finding_dictionary.to_JSON(), keyword, force_write)

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

def iterate_through_dictionary(dictionary, finding, key, depth):
    if depth == 0:
        finding.callback(finding, key, dictionary)
    else:
        for key in dictionary:
            iterate_through_dictionary(dictionary[key], finding, key, depth -1)

def load_from_json(keyword, var):
    filename = 'json/aws_' + keyword + '_' + var + '.json'
    with open(filename) as f:
        return json.load(f)

def manage_dictionary(dictionary, key, init, callback=None):
    if not str(key) in dictionary:
        dictionary[str(key)] = init
        manage_dictionary(dictionary, key, init)
        if callback:
            callback(dictionary[key])
    return dictionary

def save_json_to_file(json_blob, keyword, force_write):
    save_to_file(json_blob, keyword, force_write, False)

def save_to_file(blob, keyword, force_write, raw=True):
    print 'Saving ' + keyword + ' data...'
    if not os.path.exists('json'):
        os.makedirs('json')
    filename = 'json/aws_' + keyword.lower().replace(' ','_') + '.json'
    if not os.path.isfile(filename) or force_write:
        with open(filename, 'wt') as f:
            print 'Success: saved data to ' + filename
            if raw:
                print >>f, json.dumps(blob, indent=4, separators=(',', ': '), sort_keys=True)
            else:
                print >>f, blob
    else:
        print 'Error: ' + filename + ' already exists.'

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
    if total and total != 0 or current != 0:
        sys.stdout.write('\n')
