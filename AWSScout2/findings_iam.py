#!/usr/bin/env python

# Import AWS Scout2 finding-related classes
from AWSScout2.finding import Finding
from AWSScout2.finding_dictionary import FindingDictionary


########################################
# IAM-related findings
########################################
iam_finding_dictionary = FindingDictionary()
iam_finding_dictionary['violations'] = []
iam_finding_dictionary['violations'].append(Finding(
    'Lack of key rotation',
    'users',
    Finding.checkAccessKeys,
    None,
    'access-key',
    'danger',
))
iam_finding_dictionary['violations'].append(Finding(
    'Lack of MFA',
    'users',
    Finding.lacksMFA,
    None,
    'mfa-enabled',
    'danger',
))
iam_finding_dictionary['violations'].append(Finding(
    'Password and keys enabled',
    'users',
    Finding.passwordAndKeyEnabled,
    None,
    'password-and-key-enabled',
    'warning',
))
