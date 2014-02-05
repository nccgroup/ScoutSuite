#!/usr/bin/env python

# Import AWS Scout2 finding-related classes
from AWSScout2.finding import Finding
from AWSScout2.finding_dictionary import FindingDictionary


########################################
# S3-related findings
########################################
s3_finding_dictionary = FindingDictionary()
s3_finding_dictionary['violations'] = []
s3_finding_dictionary['violations'].append(Finding(
    'Bucket world-writable',
    'buckets',
    None,
    None,
    'internet-accessible-port',
    'warning'
))
