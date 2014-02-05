#!/usr/bin/env python

# Import AWS Scout2 finding-related classes
from AWSScout2.finding import Finding
from AWSScout2.finding_dictionary import FindingDictionary


########################################
# EC2-related findings
########################################
ec2_finding_dictionary = FindingDictionary()
ec2_finding_dictionary['violations'] = []
ec2_finding_dictionary['violations'].append(Finding(
    'SSH open to Internet',
    'groups',
    Finding.checkInternetAccessiblePort,
    '22',
    'internet-accessible-port',
    'danger',
))
#finding_dictionary['ec2'] = FindingDictionary()
#finding_dictionary['ec2'].append({
#    'SSH open to Internet'
#})
#finding_dictionary['ec2'].append({
#    'RDP open to Internet'
#})
#finding_dictionary['ec2'].append({
#    'Use of plaintext protocols #23 #21..'
#})
