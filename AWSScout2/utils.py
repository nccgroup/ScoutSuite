#!/usr/bin/env python2

# Import AWSUtils
from AWSUtils.utils import *

# Import third-party packages
import argparse
import boto
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
supported_services = ['cloudtrail', 'ec2', 'iam', 'rds', 's3']

########################################
##### Argument parser
########################################

init_parser()
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

class Scout2Encoder(json.JSONEncoder):
    def default(self, o):
        return o.__dict__


########################################
# Violations search functions
########################################

def analyze_config(finding_dictionary, filter_dictionary, config, keyword, force_write):
    # Filters
    try:
        for key in filter_dictionary:
            f = filter_dictionary[key]
            entity_path = f.entity.split('.')
            process_finding(config, f)
        config['filters'] = filter_dictionary
    except Exception, e:
        printException(e)
        pass
    # Violations
    try:
        for key in finding_dictionary:
            finding = finding_dictionary[key]
            entity_path = finding.entity.split('.')
            process_finding(config, finding)
        config['violations'] = finding_dictionary
    except Exception, e:
        printException(e)
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
        if entities in config or entities == '':
            if finding.callback:
                callback = getattr(finding, finding.callback)
                if entities in config:
                    for key in config[entities]:
                        # Dashboard: count the number of processed entities here
                        finding.checked_items = finding.checked_items + 1
                        callback(key, config[entities][key])
                else:
                    # Special case when performing a check that requires access to the whole config, leave entities empty
                    callback('foo', config)
            else:
                return
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
# File read/write functions
########################################

AWSCONFIG_DIR = 'inc-awsconfig'
REPORT_TITLE  = 'AWS Scout2 Report'

def create_new_scout_report(environment_name, force_write):
    new_dir = AWSCONFIG_DIR + '-' + environment_name
    if not os.path.exists(AWSCONFIG_DIR):
        return
    new_file = 'report-' + environment_name + '.html'
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
                    newline = line.replace(REPORT_TITLE, REPORT_TITLE + ' [' + environment_name + ']')
                    newline = newline.replace(AWSCONFIG_DIR, new_dir)
                    nf.write(newline)

def load_info_from_json(aws_service, environment_name):
    filename = AWSCONFIG_DIR
    if environment_name:
        filename = filename + '-' + environment_name
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
    return prompt_4_yes_no('File \'{}\' already exists. Do you want to overwrite it'.format(filename))

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
            write_data_to_file(f, blob, force_write)
    except Exception, e:
        printException(e)
        pass

def write_data_to_file(f, blob, force_write):
    print >>f, '%s' % json.dumps(blob, indent=4, separators=(',', ': '), sort_keys=True, cls=Scout2Encoder)


########################################
# Status update functions
########################################

def init_status(items, keyword=None, fetched=0):
    count = fetched
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
