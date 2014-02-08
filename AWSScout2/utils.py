#!/usr/bin/env python

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

def analyze_config(finding_dictionary, config, keyword):
    for finding in finding_dictionary['violations']:
        for entity in config[finding.entity + 's']:
            finding.callback(finding, entity)
    save_json_to_file(finding_dictionary.to_JSON(), keyword, True)

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
    return key_id, secret

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
    return 0, len(items)

def update_status(current, total):
    current = current + 1
    sys.stdout.write("\r %d/%d" % (current, total))
    sys.stdout.flush()
    return current

def close_status():
    sys.stdout.write('\n')
