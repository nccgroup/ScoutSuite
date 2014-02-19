#!/usr/bin/env python2

# Import AWS Scout2 finding-related classes
from AWSScout2.finding_ec2 import *
from AWSScout2.finding_iam import *
from AWSScout2.finding_s3 import *
from AWSScout2.finding_dictionary import *
from AWSScout2.utils import *

import copy
import re


########################################
# Finding dictionaries
########################################
iam_finding_dictionary = FindingDictionary()
ec2_finding_dictionary = FindingDictionary()
s3_finding_dictionary = FindingDictionary()


########################################
# Common functions
########################################

def load_default_findings(keyword):
    finding_dictionary, finding_class = get_finding_variables(keyword)
    filename = 'rules/findings-' + keyword + '.default.json'
    findings = load_findings(filename)
    for f in findings:
        if 'targets' in findings[f]:
            for t in findings[f]['targets']:
                name = set_argument_values(f, t)
                finding_dictionary[name] = finding_class(
                    set_argument_values(findings[f]['description'], t),
                    set_argument_values(findings[f]['entity'], t),
                    getattr(finding_class, findings[f]['callback']),
                    set_arguments(findings[f]['callback_args'], t),
                    set_argument_values(findings[f]['level'], t))
        else:
            finding_dictionary[f] = finding_class(
                findings[f]['description'],
                findings[f]['entity'],
                getattr(finding_class, findings[f]['callback']),
                findings[f]['callback_args'],
                findings[f]['level'])

def set_arguments(arg_names, t):
    real_args = []
    for a in arg_names:
        real_args.append(set_argument_values(a, t))
    return real_args

def set_argument_values(string, target):
    for w in string.split('-'):
        res = re.match(r'(_ARG_(\w+)_)', w)
        if res:
            i = int(res.groups()[1])
            print "%s => %s" % (res.groups()[0] , target[i])
            string = string.replace(res.groups()[0], target[i])
    return string

def get_finding_variables(keyword):
    if keyword == 'ec2':
        return ec2_finding_dictionary, Ec2Finding
    elif keyword == 'iam':
        return iam_finding_dictionary, IamFinding
    elif keyword == 's3':
        return s3_finding_dictionary, S3Finding
    else:
        return None, None


########################################
# Load findings from JSON config files
########################################
load_default_findings('ec2')
load_default_findings('iam')
load_default_findings('s3')
