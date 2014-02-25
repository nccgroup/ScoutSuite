#!/usr/bin/env python2

# Import AWS Scout2 tools
from AWSScout2.utils import *
from AWSScout2.findings import *
from AWSScout2.protocols_dict import *


# Import other third-party packages
from pprint import pprint
import traceback


########################################
##### EC2 functions
########################################

def analyze_ec2_config(ec2_info, force_write):
    print 'Analyzing EC2 data...'
    analyze_config(ec2_finding_dictionary, ec2_info, 'EC2', force_write)

def get_ec2_info(key_id, secret, session_token, fetch_ec2_gov):
    ec2_info = {}
    ec2_info['regions'] = {}
    for region in boto.ec2.regions():
        manage_dictionary(ec2_info['regions'], region.name, {})
        manage_dictionary(ec2_info['regions'][region.name], 'vpcs', {})
        try:
            # h4ck -- skip china north region as it hangs when requesting instances (https://github.com/boto/boto/issues/2083)
            if (region.name != 'us-gov-west-1' or fetch_ec2_gov) and (region.name != 'cn-north-1'):
                ec2_connection = boto.ec2.connect_to_region(region.name, aws_access_key_id = key_id, aws_secret_access_key = secret, security_token = session_token)
                vpc_connection = boto.vpc.connect_to_region(region.name, aws_access_key_id = key_id, aws_secret_access_key = secret, security_token = session_token)
                print 'Fetching EC2 data for region %s...' % region.name
                get_vpc_info(vpc_connection, ec2_info['regions'][region.name]['vpcs'])
                get_security_groups_info(ec2_connection, ec2_info['regions'][region.name]['vpcs'])
                get_instances_info(ec2_connection, ec2_info['regions'][region.name]['vpcs'])
        except Exception, e:
            print 'Exception:\n %s' % traceback.format_exc()
            pass
    return ec2_info

def get_instances_info(ec2, vpc_info):
    reservations = ec2.get_all_reservations()
    count, total = init_status(None, 'Instances')
    for reservation in reservations:
        total = total + len(reservation.instances)
        for i in reservation.instances:
            vpc_id = i.vpc_id if i.vpc_id else 'no-vpc'
            manage_dictionary(vpc_info[vpc_id], 'instances', {})
            manage_dictionary(vpc_info[vpc_id]['instances'], i.id, {})
            vpc_info[vpc_id]['instances'][i.id]['reservation_id'] = reservation.id
            # Get instance variables (see http://boto.readthedocs.org/en/latest/ref/ec2.html#module-boto.ec2.instance to see what else is available)
            for key in ['id', 'public_dns_name', 'private_dns_name', 'key_name', 'launch_time', 'private_ip_address', 'ip_address']:
                vpc_info[vpc_id]['instances'][i.id][key] = i.__dict__[key]
            # FIXME ... see why it's not working when added in the list above
            vpc_info[vpc_id]['instances'][i.id]['state'] = i.state
            manage_dictionary(vpc_info[vpc_id]['instances'][i.id], 'security_groups', [])
            for sg in i.groups:
                vpc_info[vpc_id]['instances'][i.id]['security_groups'].append(sg.id)
            count = update_status(count, total, 'Instances')
    close_status(count, total, 'Instances')

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

def get_vpc_info(vpc_connection, vpc_info):
    vpcs = vpc_connection.get_all_vpcs()
    count, total = init_status(vpcs, 'VPC')
    for vpc in vpcs:
        manage_dictionary(vpc_info, vpc.id, {})
        vpc_info[vpc.id]['state'] = vpc.state
        vpc_info[vpc.id]['is_default'] = vpc.is_default
        vpc_info[vpc.id]['cidr_block'] = vpc.cidr_block
        acls = vpc_connection.get_all_network_acls(filters ={"vpc_id": vpc.id})
        vpc_info[vpc.id]['network_acls'] = {}
        for acl in acls:
            manage_dictionary(vpc_info[vpc.id]['network_acls'], acl.id, {})
            vpc_info[vpc.id]['network_acls'][acl.id]['default'] = acl.default
            vpc_info[vpc.id]['network_acls'][acl.id]['inbound_network_acls'] = get_network_acl_entries(acl.network_acl_entries, "true")
            vpc_info[vpc.id]['network_acls'][acl.id]['outbound_network_acls'] = get_network_acl_entries(acl.network_acl_entries, "false")
        count = update_status(count, total, 'VPC')
    close_status(count, total, 'VPC')
    return vpc_info

def get_security_groups_info(ec2_connection, vpc_info):
    groups = ec2_connection.get_all_security_groups()
    count, total = init_status(groups, 'Security groups')
    for group in groups:
        vpc_id = group.vpc_id if group.vpc_id else 'no-vpc'
        manage_dictionary(vpc_info, vpc_id, {})
        manage_dictionary(vpc_info[vpc_id], 'security_groups', {})
        manage_dictionary(vpc_info[vpc_id]['security_groups'], group.name, {})
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
        vpc_info[vpc_id]['security_groups'][group.name] = security_group
        count = update_status(count, total, 'Security groups')
    close_status(count, total, 'Security groups')
