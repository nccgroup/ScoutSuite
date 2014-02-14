#!/usr/bin/env python2

# Import AWS Scout2 finding-related classes
from AWSScout2.finding_iam import *
from AWSScout2.finding_dictionary import *


########################################
# IAM-related findings
########################################
iam_finding_dictionary = FindingDictionary()
iam_finding_dictionary['Active-key-no-rotation'] = IamFinding(
    'Lack of key rotation',
    'user',
    IamFinding.checkAccessKeys,
    'Active',
    'danger',
)
iam_finding_dictionary['Inactive-key-no-rotation'] = IamFinding(
    'Lack of key rotation',
    'user',
    IamFinding.checkAccessKeys,
    'Inactive',
    'warning',
)
iam_finding_dictionary['no-mfa'] = IamFinding(
    'Lack of MFA',
    'user',
    IamFinding.lacksMFA,
    None,
    'danger',
)
iam_finding_dictionary['password-and-key'] = IamFinding(
    'Password and keys enabled',
    'user',
    IamFinding.passwordAndKeyEnabled,
    None,
    'warning',
)
