#!/usr/bin/env python2

# Import AWS Scout2 finding-related classes
from AWSScout2.finding_ec2 import *
from AWSScout2.finding_dictionary import *


########################################
# EC2-related findings
########################################
ec2_finding_dictionary = FindingDictionary()
ec2_finding_dictionary['violations'] = []

# Ports that should not be accessible to public IP addresses
rc_ports = [
    ['SSH open to Internet', 'ssh-port-public', ('tcp', '22')],
    ['RDP open to Internet', 'rdp-port-public', ('tcp', '3389')],
    ['MySQL open to Internet', 'mysql-port-public', ('tcp', '3306')],
    ['Ms SQL open to Internet', 'mssql-port-public', ('tcp', '1433')],
]
for port in rc_ports:
    ec2_finding_dictionary['violations'].append(Ec2Finding(
        port[0],
        port[1],
        'region.vpc.security_group',
        Ec2Finding.checkInternetAccessiblePort,
        ['blacklist', port[2]],
        '',
        'danger',
    ))


# Plaintext protocols
plaintext_ports = [
    ['FTP (plaintext)', 'ftp', ('tcp', '21')],
    ['Telnet (plaintext)', 'telnet', ('tcp', '23')],
]
for port in plaintext_ports:
    ec2_finding_dictionary['violations'].append(Ec2Finding(
        port[0],
        port[1],
        'region.vpc.security_group',
        Ec2Finding.checkOpenPort,
        port[2],
        '',
        'danger',
    ))

# Publicly accessible ports
wl_ports = ['80', '443']
for rcp in rc_ports:
    wl_ports.append(rcp[2][1])
ec2_finding_dictionary['violations'].append(Ec2Finding(
    'Ports open to Internet',
    'public-ports',
    'region.vpc.security_group',
    Ec2Finding.checkInternetAccessiblePort,
    ['whitelist', ('tcp', wl_ports)],
    '',
    'warning',
))
