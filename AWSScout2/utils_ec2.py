#!/usr/bin/env python

# Import AWS Scout2 tools
from AWSScout2.utils import *
from AWSScout2.findings_ec2 import *


########################################
##### EC2 functions
########################################

def analyze_ec2_config(instances, security_groups):
    print 'Analyzing EC2 data...'
    ec2_config = {"instances": instances['instances'], "security_groups": security_groups['security_groups']}
    analyze_config(ec2_finding_dictionary, ec2_config, 'EC2 violations')

def get_security_groups_info(ec2, region):
    groups = ec2.get_all_security_groups()
    security_groups = []
    for group in groups:
        security_group = {}
        security_group['name'] = group.name
        security_group['id'] = group.id
        security_group['description'] = group.description
        security_group = manage_dictionary(security_group, 'running-instances', [])
        security_group = manage_dictionary(security_group, 'stopped-instances', [])
        protocols = {}
        for rule in group.rules:
            protocols = manage_dictionary(protocols, rule.ip_protocol, {})
            protocols[rule.ip_protocol] = manage_dictionary(protocols[rule.ip_protocol], 'rules', [])
            protocols[rule.ip_protocol]['name'] = rule.ip_protocol.upper()
            acl = {}
            acl['grants'] = []
            # Save grants, values are either a CIDR or an EC2 security group
            for grant in rule.grants:
                if grant.cidr_ip:
                    acl['grants'].append(grant.cidr_ip)
                else:
                    acl['grants'].append('%s (%s)' % (grant.name, grant.groupId))
            # Save the port (single port or range)
            if rule.from_port == rule.to_port:
                acl['ports'] = rule.from_port
            else:
                acl['ports'] = '%s-%s' % (rule.from_port, rule.to_port)
            # Save the new rule
            protocols[rule.ip_protocol]['rules'].append(acl)
        # Save all the rules, sorted by protocol
        security_group['protocols'] = protocols
        # Save all instances associated with this group
        for i in group.instances():
            if i.state == 'running':
                security_group['running-instances'].append(i.id)
            else:
                security_group['stopped-instances'].append(i.id)
        # Append the new security group to the return list
        security_groups.append(security_group)
    return security_groups

def get_instances_info(ec2, region):
    results = []
    reservations = ec2.get_all_reservations()
    for reservation in reservations:
        groups = []
        for g in reservation.groups:
            groups.append(g.name)
        for i in reservation.instances:
            instance = {}
            instance['reservation_id'] = reservation.id
            instance['groups'] = groups
            instance['region'] = region
            # Get instance variables (see http://boto.readthedocs.org/en/latest/ref/ec2.html#module-boto.ec2.instance to see what else is available)
            for key in ['id', 'public_dns_name', 'private_dns_name', 'key_name', 'launch_time', 'private_ip_address', 'ip_address']:
                instance[key] = i.__dict__[key]
            # FIXME ... see why it's not working when added in the list above
            instance['state'] = i.state
            results.append(instance)
    return results
