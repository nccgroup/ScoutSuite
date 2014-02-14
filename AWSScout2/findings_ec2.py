#!/usr/bin/env python2

# Import AWS Scout2 finding-related classes
from AWSScout2.finding_ec2 import *
from AWSScout2.finding_dictionary import *


########################################
# EC2-related findings
########################################
ec2_finding_dictionary = FindingDictionary()

# Ports that should not be accessible to public IP addresses
rc_ports = [
    ['SSH open to Internet', ('tcp', '22')],
    ['RDP open to Internet', ('tcp', '3389')],
    ['MySQL open to Internet', ('tcp', '3306')],
    ['Ms SQL open to Internet', ('tcp', '1433')],
]

for port in rc_ports:
    rule_name = port[1][0].upper() + '-' + port[1][1] + '-0.0.0.0/0'
    ec2_finding_dictionary[rule_name] = Ec2Finding(
        port[0],
        'region.vpc.security_group',
        Ec2Finding.checkInternetAccessiblePort,
        ['blacklist', port[1]],
        '',
        'danger',
    )


# Plaintext protocols
plaintext_ports = [
    ['FTP (plaintext)', ('tcp', '21')],
    ['Telnet (plaintext)', ('tcp', '23')],
]
for port in plaintext_ports:
    rule_name = port[1][0].upper() + '-' + port[1][1]
    ec2_finding_dictionary[rule_name] = Ec2Finding(
        port[0],
        'region.vpc.security_group',
        Ec2Finding.checkOpenPort,
        port[1],
        '',
        'danger',
    )

# Publicly accessible ports
wl_ports = ['80', '443']
for rcp in rc_ports:
    wl_ports.append(rcp[1][1])

ec2_finding_dictionary['public-ports'] = Ec2Finding(
    'Ports open to Internet',
    'region.vpc.security_group',
    Ec2Finding.checkInternetAccessiblePort,
    ['whitelist', ('tcp', wl_ports)],
    '',
    'warning',
)
