#!/usr/bin/env python2

# Import AWS Scout2 tools
from AWSScout2.utils import *
from AWSScout2.findings_ec2 import *
from AWSScout2.protocols_dict import *


########################################
##### EC2 functions
########################################

def analyze_ec2_config(instances, security_groups, network_acls, force_write):
    print 'Analyzing EC2 data...'
    ec2_config = {"instances": instances, "security_groups": security_groups, "network_acls": network_acls}
    analyze_config(ec2_finding_dictionary, ec2_config, 'EC2 violations', force_write)

def get_instances_info(ec2, region):
    instances = {}
    reservations = ec2.get_all_reservations()
    count, total = init_status(None)
    for reservation in reservations:
        groups = []
        for g in reservation.groups:
            groups.append(g.name)
        for i in reservation.instances:
            count = update_status(count, total)
            manage_dictionary(instances, i.id, {})
            instances[i.id]['reservation_id'] = reservation.id
            instances[i.id]['groups'] = groups
            instances[i.id]['region'] = region
            # Get instance variables (see http://boto.readthedocs.org/en/latest/ref/ec2.html#module-boto.ec2.instance to see what else is available)
            for key in ['id', 'public_dns_name', 'private_dns_name', 'key_name', 'launch_time', 'private_ip_address', 'ip_address']:
                instances[i.id][key] = i.__dict__[key]
            # FIXME ... see why it's not working when added in the list above
            instances[i.id]['state'] = i.state
    close_status(count, total)
    return instances

def get_network_acl_entries(entries, egress):
    acl_list = []
    for entry in entries:
        if entry.egress == egress:
            acl = {}
            for key in ['cidr_block', 'rule_action', 'rule_number']:
                acl[key] = entry.__dict__[key]
            from_port = entry.port_range.from_port if entry.port_range.from_port else 1
            to_port = entry.port_range.to_port if entry.port_range.to_port else 65535
            acl['port_range'] = from_port if from_port == to_port else str(from_port) + '-' + str(to_port)
            acl['protocol'] = protocols_dict[entry.protocol]
            acl_list.append(acl)
    return acl_list

def get_network_acls_info(vpc_connection):
    network_acls_info = {}
    vpcs = vpc_connection.get_all_vpcs()
    count, total = init_status(vpcs)
    for vpc in vpcs:
        manage_dictionary(network_acls_info, vpc.id, {})
        network_acls_info[vpc.id]['state'] = vpc.state
        network_acls_info[vpc.id]['is_default'] = vpc.is_default
        network_acls_info[vpc.id]['cidr_block'] = vpc.cidr_block
        acls = vpc_connection.get_all_network_acls(filters ={"vpc_id": vpc.id})
        network_acls_info[vpc.id]['network_acls'] = {}
        for acl in acls:
            manage_dictionary(network_acls_info[vpc.id]['network_acls'], acl.id, {})
            network_acls_info[vpc.id]['network_acls'][acl.id]['default'] = acl.default
            network_acls_info[vpc.id]['network_acls'][acl.id]['inbound_network_acls'] = get_network_acl_entries(acl.network_acl_entries, "true")
            network_acls_info[vpc.id]['network_acls'][acl.id]['outbound_network_acls'] = get_network_acl_entries(acl.network_acl_entries, "false")
    return network_acls_info

def get_security_groups_info(ec2, region):
    groups = ec2.get_all_security_groups()
    security_groups = {}
    count, total = init_status(groups)
    for group in groups:
        vpc_id = group.vpc_id if group.vpc_id else 'no-vpc'
        manage_dictionary(security_groups, vpc_id, {})
        manage_dictionary(security_groups[vpc_id], group.name, {})
        count = update_status(count, total)
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
        security_groups[vpc_id][group.name] = security_group
    close_status(count, total)
    return security_groups
