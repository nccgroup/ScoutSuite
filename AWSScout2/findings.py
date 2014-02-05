#!/usr/bin/env python

# Import AWS Scout2 tools
from AWSScout2.utils import *
from AWSScout2.finding import Finding


# JSON-serializable finding dictionary
class FindingDictionary(dict):

    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)


########################################
# EC2-related findings
########################################
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


########################################
# IAM-related findings
########################################
iam_finding_dictionary = FindingDictionary()
iam_finding_dictionary['violations'] = []
iam_finding_dictionary['violations'].append(Finding(
    'Lack of key rotation',
    'danger',
    'users',
    Finding.checkAccessKeys,
    'access-key'
))
iam_finding_dictionary['violations'].append(Finding(
    'Lack of MFA',
    'danger',
    'users',
    Finding.lacksMFA,
    'mfa-enabled'
))
iam_finding_dictionary['violations'].append(Finding(
    'Password and keys enabled.',
    'warning',
    'users',
    Finding.passwordAndKeyEnabled,
    'password-and-key-enabled'
))


########################################
# S3-related findings
########################################
#finding_dictionary['s3'] = FindingDictionary()
#finding_dictionary['s3']['violations'].append(Finding(
#    'Bucket world-writable'
#})
