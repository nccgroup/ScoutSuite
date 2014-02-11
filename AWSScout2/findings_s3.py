#!/usr/bin/env python2

# Import AWS Scout2 finding-related classes
from AWSScout2.finding_s3 import *
from AWSScout2.finding_dictionary import *


########################################
# S3-related findings
########################################
s3_finding_dictionary = FindingDictionary()
s3_finding_dictionary['violations'] = []
s3_finding_dictionary['violations'].append(S3Finding(
    'Bucket world-writable',
    'bucket-write',
    'bucket',
    S3Finding.checkWorldWritableBucket,
    None,
    '',
    'danger'
))
s3_finding_dictionary['violations'].append(S3Finding(
    'Bucket world-readable',
    'bucket-read',
    'bucket',
    S3Finding.checkWorldReadableBucket,
    None,
    '',
    'warning'
))
