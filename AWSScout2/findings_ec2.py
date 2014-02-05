#!/usr/bin/env python

# Import AWS Scout2 finding-related classes
from AWSScout2.finding import Finding
from AWSScout2.finding_dictionary import FindingDictionary


########################################
# EC2-related findings
########################################
ec2_finding_dictionary = FindingDictionary()
ec2_finding_dictionary['violations'] = []

# Ports that should not be accessible to public IP addresses
rc_ports = [
    ['SSH open to Internet', ('tcp', '22')],
    ['RDP open to Internet', ('tcp', '3389')],
]
for port in rc_ports:
    ec2_finding_dictionary['violations'].append(Finding(
        port[0],
        'security_groups',
        Finding.checkInternetAccessiblePort,
        port[1],
        '',
        'danger',
    ))


# Plaintext protocols
plaintext_ports = [
    ['FTP (plaintext)', ('tcp', '21')],
    ['Telnet (plaintext)', ('tcp', '23')],
]
for port in plaintext_ports:
    ec2_finding_dictionary['violations'].append(Finding(
        port[0],
        'security_groups',
        Finding.checkOpenPort,
        port[1],
        '',
        'danger',
    ))
