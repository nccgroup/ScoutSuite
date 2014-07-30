#!/usr/bin/env python2

# Import the Amazon SDK
import boto

# Import other third-party packages
import argparse
from distutils import dir_util
import copy
import json
import os
import re
import requests
import shutil
import sys
import traceback
import urllib2


########################################
# Globals
########################################
supported_services = ['cloudtrail', 'ec2', 'iam', 's3']


########################################
# Common parameters
########################################

parser = argparse.ArgumentParser()

parser.add_argument('--force',
                    dest='force_write',
                    default=False,
                    action='store_true',
                    help='overwrite existing json files')
parser.add_argument('--ruleset_name',
                    dest='ruleset_name',
                    default='default',
                    nargs='+',
                    help='Customized set of rules')
parser.add_argument('--services',
                    dest='services',
                    default=supported_services,
                    nargs='+',
                    help='Name of services you want to analyze')
parser.add_argument('--skip',
                    dest='skipped_services',
                    default=[],
                    nargs='+',
                    help='Name of services you want to ignore')


########################################
# Common functions
########################################

def build_services_list(services, skipped_services):

    enabled_services = []
    for s in services:
        if s in supported_services and s not in skipped_services:
            enabled_services.append(s)
    return enabled_services

def check_boto_version():
    min_boto_version = '2.31.1'
    latest_boto_version = 0
    if boto.Version < min_boto_version:
        print 'Error: the version of boto installed on this system (%s) is too old. Boto version %s or newer is required.' % (boto.Version, min_boto_version)
        return False
    else:
        # Warn users who have not the latest version of boto installed
        release_tag_regex = re.compile('(\d+)\.(\d+)\.(\d+)')
        tags = requests.get('https://api.github.com/repos/boto/boto/tags').json()
        for tag in tags:
            if release_tag_regex.match(tag['name']) and tag['name'] > latest_boto_version:
                latest_boto_version = tag['name']
        if boto.Version < latest_boto_version:
            print 'Warning: the version of boto installed (%s) is not the latest available (%s). Consider upgrading to ensure that all features are enabled.' % (boto.Version, latest_boto_version)
    return True

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

def has_instances(ec2_region):
    count = 0
    for v in ec2_region['vpcs']:
        if 'instances' in ec2_region['vpcs'][v]:
            count = count + len(ec2_region['vpcs'][v]['instances'])
    return False if count == 0 else True

def match_instances_and_roles(ec2_config, iam_config):
    role_instances = {}
    for r in ec2_config['regions']:
        for v in ec2_config['regions'][r]['vpcs']:
            if 'instances' in ec2_config['regions'][r]['vpcs'][v]:
                for i in ec2_config['regions'][r]['vpcs'][v]['instances']:
                    arn = ec2_config['regions'][r]['vpcs'][v]['instances'][i]['profile_arn']
                    if arn:
                        manage_dictionary(role_instances, arn, [])
                        role_instances[arn].append(i)
    for role in iam_config['roles']:
        for arn in iam_config['roles'][role]['instance_profiles']:
            if arn in role_instances:
                iam_config['roles'][role]['instance_profiles'][arn]['instances'] = role_instances[arn]

def process_entities(config, finding, entity_path):
    if len(entity_path) == 1:
        entities = entity_path.pop(0)
        if entities in config:
            callback = getattr(finding, finding.callback)
            for key in config[entities]:
                callback(key, config[entities][key])
    elif len(entity_path) != 0:
        entities = entity_path.pop(0)
        for key in config[entities]:
            process_entities(config[entities][key], finding, copy.deepcopy(entity_path))
    else:
        print 'Unknown error'

def process_finding(config, finding):
    entity_path = finding.entity.split('.')
    process_entities(config, finding, entity_path)

def refine_cloudtrail(cloudtrail_config, ec2_config):
    inactive_regions = [r for r in cloudtrail_config['violations']['Service disabled'].items]
    for r in inactive_regions:
        cloudtrail_config['violations']['Service disabled'].removeItem(r)


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
    mfa_serial = None
    with open(filename, 'rt') as csvfile:
        for i, line in enumerate(csvfile):
            if i == 1:
                try:
                    username, key_id, secret = line.split(',')
                except:
                    try:
                        username, key_id, secret, mfa_serial = line.split(',')
                        mfa_serial = mfa_serial.rstrip()
                    except:
                        print 'Error, the CSV file is not properly formatted'
    return key_id.rstrip(), secret.rstrip(), mfa_serial

def fetch_sts_credentials(key_id, secret, mfa_serial, mfa_code):
    if not mfa_serial or len(mfa_serial) < 1:
        print 'Error, you need to provide your MFA device\'s serial number.'
        return None, None, None
    if not mfa_code or len(mfa_code) < 1:
        print 'Error, you need to provide the code displayed by your MFA device.'
        return None, None, None
    sts_connection = boto.connect_sts(key_id, secret)
    # For now, don't set the duration and use default 12hours
    sts_response = sts_connection.get_session_token(mfa_serial_number = mfa_serial, mfa_token = mfa_code[0])
    return sts_response.access_key, sts_response.secret_key, sts_response.session_token


########################################
# File read/write functions
########################################

AWSCONFIG_DIR = 'inc-awsconfig'
REPORT_TITLE  = 'AWS Scout2 Report'

def create_new_scout_report(environment_name, force_write):
    new_dir = AWSCONFIG_DIR + '-' + environment_name[0]
    new_file = 'report-' + environment_name[0] + '.html'
    print 'Creating %s ...' % new_file
    if prompt_4_overwrite(new_dir, force_write):
        if not os.path.exists(new_dir):
            os.makedirs(new_dir)
        dir_util.copy_tree(AWSCONFIG_DIR, new_dir, update = force_write)
        shutil.rmtree(AWSCONFIG_DIR)
        if os.path.exists(new_file):
            os.remove(new_file)
        with open('report.html') as f:
            with open(new_file, 'wt') as nf:
                for line in f:
                    newline = line.replace(REPORT_TITLE, REPORT_TITLE + ' [' + environment_name[0] + ']')
                    newline = newline.replace(AWSCONFIG_DIR, new_dir)
                    nf.write(newline)

def load_info_from_json(aws_service, environment_name):
    filename = AWSCONFIG_DIR
    if environment_name:
        filename = filename + '-' + environment_name[0]
    filename = filename + '/' + aws_service + '_config.js'
    with open(filename) as f:
        json_payload = f.readlines()
        json_payload.pop(0)
        json_payload = ''.join(json_payload)
        return json.loads(json_payload)

def load_from_json(keyword, var):
    filename = AWSCONFIG_DIR + '/' + keyword + '_config.js'
    with open(filename) as f:
        json_payload = f.readlines()
        json_payload.pop(0)
        json_payload = ''.join(json_payload)
        return json.loads(json_payload)

def open_file(keyword, force_write):
    out_dir = AWSCONFIG_DIR
    print 'Saving ' + keyword + ' data...'
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    filename = out_dir + '/' + keyword.lower().replace(' ','_') + '_config.js'
    if prompt_4_overwrite(filename, force_write):
       return open(filename, 'wt')
    else:
        return None

def prompt_4_yes_no(question):
    while True:
        sys.stdout.write(question + ' (y/n)? ')
        choice = raw_input().lower()
        if choice == 'yes' or choice == 'y':
            return True
        elif choice == 'no' or choice == 'n':
            return False
        else:
            print '\'%s\' is not a valid answer. Enter \'yes\'(y) or \'no\'(n).' % choice

def prompt_4_overwrite(filename, force_write):
    # Do not prompt if the file does not exist or force_write is set
    if not os.path.exists(filename) or force_write:
        return True
    return prompt_4_yes_no('File already exists. Do you want to overwrite it')

def prompt_4_value(question, choices = None, default = None):
    if choices:
        question = question + ' (' + '/'.join(choices) + ')'
    while True:
        sys.stdout.write(question + '? ')
        choice = raw_input()
        if choices:
            if choice in choices:
                return choice
            else:
                print 'Invalid value.'
        elif not choice and default:
            if prompt_4_yes_no('Use the default value (' + default + ')'):
                return default
        elif not choice:
            print 'You cannot leave this parameter empty.'
        elif prompt_4_yes_no('You entered "' + choice + '". Is that correct'):
            return choice

def save_blob_to_file(filename, blob, force_write):
    try:
        if prompt_4_overwrite(filename, force_write):
            with open(filename, 'wt') as f:
                write_data_to_file(f, blob, force_write)
    except:
        pass

def save_config_to_file(blob, keyword, force_write):
    try:
        with open_file(keyword, force_write) as f:
            keyword = keyword.lower().replace(' ','_')
            print >>f, keyword + '_info ='
            keyword = write_data_to_file(f, blob, force_write)
    except:
        pass

def write_data_to_file(f, blob, force_write):
    print >>f, '%s' % json.dumps(blob, indent=4, separators=(',', ': '), sort_keys=True, cls=Scout2Encoder)


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
    return current + 1

def close_status(current, total, keyword=None):
    update_status(current, total, keyword)
    sys.stdout.write('\n')
