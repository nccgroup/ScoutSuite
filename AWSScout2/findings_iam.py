#!/usr/bin/env python2

# Import AWS Scout2 finding-related classes
from AWSScout2.finding_iam import *
from AWSScout2.finding_dictionary import *


########################################
# IAM-related findings
########################################
iam_finding_dictionary = FindingDictionary()
iam_finding_dictionary['violations'] = []
iam_finding_dictionary['violations'].append(IamFinding(
    'Lack of key rotation',
    'rotation',
    'user',
    IamFinding.checkAccessKeys,
    'Active',
    'access-key',
    'danger',
))
iam_finding_dictionary['violations'].append(IamFinding(
    'Lack of key rotation',
    'rotation',
    'user',
    IamFinding.checkAccessKeys,
    'Inactive',
    'access-key',
    'warning',
))
iam_finding_dictionary['violations'].append(IamFinding(
    'Lack of MFA',
    'mfa',
    'user',
    IamFinding.lacksMFA,
    None,
    'mfa-enabled',
    'danger',
))
iam_finding_dictionary['violations'].append(IamFinding(
    'Password and keys enabled',
    'password-and-key',
    'user',
    IamFinding.passwordAndKeyEnabled,
    None,
    'password-and-key-enabled',
    'warning',
))
