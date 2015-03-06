#!/usr/bin/env python2

# Import the Amazon SDK
import boto
from boto import ec2
from boto import vpc
from boto.ec2 import elb

# Import AWS Scout2 tools
from AWSScout2.utils import *
from AWSScout2.filters import *
from AWSScout2.findings import *
from AWSScout2.protocols_dict import *


########################################
##### EC2 analysis functions
########################################

def analyze_ec2_config(ec2_info, force_write):
    print 'Analyzing EC2 data...'
    analyze_config(ec2_finding_dictionary, ec2_filter_dictionary, ec2_info, 'EC2', force_write)
    # Custom EC2 analysis
    check_for_elastic_ip(ec2_info)
    link_elastic_ips(ec2_info)
    list_network_attack_surface(ec2_info)
    save_config_to_file(ec2_info, 'EC2', force_write)


#
# Check that the whitelisted EC2 IP addresses are not static IPs
#
def check_for_elastic_ip(ec2_info):
    # Build a list of all elatic IP in the account
    elastic_ips = []
    for region in ec2_info['regions']:
        if 'elastic_ips' in ec2_info['regions'][region]:
            for eip in ec2_info['regions'][region]['elastic_ips']:
                elastic_ips.append(eip)
    new_items = []
    new_macro_items = []
    for i, item in enumerate(ec2_info['violations']['non-elastic-ec2-public-ip-whitelisted'].items):
        ip = netaddr.IPNetwork(item)
        found = False
        for eip in elastic_ips:
            eip = netaddr.IPNetwork(eip)
            if ip in eip:
                found = True
                break
        if not found:
            new_items.append(ec2_info['violations']['non-elastic-ec2-public-ip-whitelisted'].items[i])
            new_macro_items.append(ec2_info['violations']['non-elastic-ec2-public-ip-whitelisted'].macro_items[i])
    ec2_info['violations']['non-elastic-ec2-public-ip-whitelisted'].items = new_items
    ec2_info['violations']['non-elastic-ec2-public-ip-whitelisted'].macro_items = new_macro_items


#
# Link EIP with instances
#
def link_elastic_ips(ec2_info):
    for r in ec2_info['regions']:
        if 'elastic_ips' in ec2_info['regions'][r]:
            for eip in ec2_info['regions'][r]['elastic_ips']:
                for v in ec2_info['regions'][r]['vpcs']:
                    if 'instances' in ec2_info['regions'][r]['vpcs'][v]:
                        for i in ec2_info['regions'][r]['vpcs'][v]['instances']:
                            if i == ec2_info['regions'][r]['elastic_ips'][eip]['instance_id']:
                                if not ec2_info['regions'][r]['vpcs'][v]['instances'][i]['ip_address']:
                                    ec2_info['regions'][r]['vpcs'][v]['instances'][i]['ip_address'] = eip
                                elif ec2_info['regions'][r]['vpcs'][v]['instances'][i]['ip_address'] != eip:
                                    print 'Warning: public IP address exists (%s) for an instance associated with an elastic IP (%s)' % (ec2_info['regions'][r]['vpcs'][v]['instances'][i]['ip_address'], eip)

#
# List the publicly available IPs/Ports
#
def list_network_attack_surface(ec2_info):
    ec2_info['attack_surface'] = {}
    for r in ec2_info['regions']:
        for v in ec2_info['regions'][r]['vpcs']:
            if 'instances' in ec2_info['regions'][r]['vpcs'][v]:
                for i in ec2_info['regions'][r]['vpcs'][v]['instances']:
                    instance = ec2_info['regions'][r]['vpcs'][v]['instances'][i]
                    if instance['ip_address']:
                        ec2_info['attack_surface'][instance['ip_address']] = {}
                        ec2_info['attack_surface'][instance['ip_address']]['protocols'] = {}
                        for sgid in instance['security_groups']:
                            sg = ec2_info['regions'][r]['vpcs'][v]['security_groups'][sgid]
                            for p in sg['rules_ingress']:
                                for ru in sg['rules_ingress'][p]['rules']:
                                    port = ru['ports']
                                    if 'cidrs' in ru['grants'] and port:
                                        manage_dictionary(ec2_info['attack_surface'][instance['ip_address']]['protocols'], p, {})
                                        manage_dictionary(ec2_info['attack_surface'][instance['ip_address']]['protocols'][p], port, {})
                                        manage_dictionary(ec2_info['attack_surface'][instance['ip_address']]['protocols'][p][port], 'cidrs', [])
                                        for cidr in ru['grants']['cidrs']:
                                            ec2_info['attack_surface'][instance['ip_address']]['protocols'][p][port]['cidrs'].append(cidr)
                                    elif not port:
                                        print instance['ip_address']
                                        print ru


########################################
##### EC2 fetch functions
########################################

def get_ec2_info(key_id, secret, session_token, fetch_ec2_gov):
    ec2_info = {}
    ec2_info['regions'] = {}
    # Build region list for each EC2 service
    ec2_regions = build_region_list(boto.ec2.regions(), ec2_info, fetch_ec2_gov)
    elb_regions = build_region_list(boto.ec2.elb.regions(), ec2_info, fetch_ec2_gov)
    vpc_regions = build_region_list(boto.vpc.regions(), ec2_info, fetch_ec2_gov)
    for region in ec2_info['regions']:
        try:
            print 'Fetching EC2 data for region %s...' % region
            # VPC
            if region in vpc_regions:
                vpc_connection = boto.vpc.connect_to_region(region, aws_access_key_id = key_id, aws_secret_access_key = secret, security_token = session_token)
                manage_dictionary(ec2_info['regions'][region], 'vpcs', {})
                get_vpc_info(vpc_connection, ec2_info['regions'][region]['vpcs'])
            # Security groups and instances
            if region in ec2_regions:
                ec2_connection = boto.ec2.connect_to_region(region, aws_access_key_id = key_id, aws_secret_access_key = secret, security_token = session_token)
                manage_dictionary(ec2_info['regions'][region], 'vpcs', {})
                get_security_groups_info(ec2_connection, ec2_info['regions'][region]['vpcs'])
                get_instances_info(ec2_connection, ec2_info['regions'][region]['vpcs'])
                get_elastic_ip_info(ec2_connection, ec2_info['regions'][region])
            # ELB
            if region in elb_regions:
                elb_connection = boto.ec2.elb.connect_to_region(region, aws_access_key_id = key_id, aws_secret_access_key = secret, security_token = session_token)
                get_elb_info(elb_connection, ec2_info['regions'][region])
        except Exception, e:
            printException(e)
            pass
    return ec2_info

def get_elastic_ip_info(ec2_connection, region_info):
    eips = ec2_connection.get_all_addresses()
    if len(eips):
        manage_dictionary(region_info, 'elastic_ips', {})
        for eip in eips:
            ip = eip.public_ip
            manage_dictionary(region_info['elastic_ips'], ip, {})
            for key in ['instance_id', 'domain', 'allocation_id', 'association_id', 'network_interface_id', 'network_interface_owner_id', 'private_ip_address']:
                region_info['elastic_ips'][ip][key] = eip.__dict__[key]

def get_elb_info(elb_connection, region_info):
    load_balancers = elb_connection.get_all_load_balancers()
    count, total = init_status(None, 'ELB')
    for lb in load_balancers:
        manage_dictionary(region_info, 'elbs', {})
        manage_dictionary(region_info['elbs'], lb.name, {})
        for key in ['dns_name', 'created_time', 'availability_zones', 'canonical_hosted_zone_name', 'canonical_hosted_zone_name_id', 'name', 'security_groups', 'subnets', 'vpc_id']:
            region_info['elbs'][lb.name][key] = lb.__dict__[key]
        manage_dictionary(region_info['elbs'][lb.name], 'listeners', {})
        for l in lb.listeners:
            port = str(l.load_balancer_port)
            manage_dictionary(region_info['elbs'][lb.name]['listeners'], port, {})
            for key in ['load_balancer_port', 'instance_port', 'protocol', 'instance_protocol', 'ssl_certificate_id', 'policy_names']:
                region_info['elbs'][lb.name]['listeners'][port][key] = l.__dict__[key]
        manage_dictionary(region_info['elbs'][lb.name], 'instances', [])
        for i in lb.instances:
            region_info['elbs'][lb.name]['instances'].append(i.id)
        manage_dictionary(region_info['elbs'][lb.name], 'source_security_group', {})
        region_info['elbs'][lb.name]['source_security_group']['name'] = lb.source_security_group.name
        region_info['elbs'][lb.name]['source_security_group']['owner_alias'] = lb.source_security_group.owner_alias
        count = update_status(count, total, 'ELB')
    close_status(count, total, 'ELB')

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
            for key in ['id', 'public_dns_name', 'private_dns_name', 'key_name', 'launch_time', 'private_ip_address', 'ip_address', 'instance_type']:
                vpc_info[vpc_id]['instances'][i.id][key] = i.__dict__[key]
            # Get instance name
            if 'Name' in i.tags and i.tags['Name'] != '':
                vpc_info[vpc_id]['instances'][i.id]['name'] = i.tags['Name']
            else:
                vpc_info[vpc_id]['instances'][i.id]['name'] = i.id
            # FIXME ... see why it's not working when added in the list above
            vpc_info[vpc_id]['instances'][i.id]['state'] = i.state
            vpc_info[vpc_id]['instances'][i.id]['profile_arn'] = i.instance_profile['arn'] if i.instance_profile else ''
            manage_dictionary(vpc_info[vpc_id]['instances'][i.id], 'security_groups', [])
            for sg in i.groups:
                vpc_info[vpc_id]['instances'][i.id]['security_groups'].append(sg.id)
            # Network interfaces
            vpc_info[vpc_id]['instances'][i.id]['interfaces'] = []
            for interface in i.interfaces:
                vpc_info[vpc_id]['instances'][i.id]['interfaces'].append(interface.id)
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
        # h4ck : data redundancy because I can't call ../@key in Handlebars
        vpc_info[vpc.id]['id'] = vpc.id
        vpc_info[vpc.id]['state'] = vpc.state
        vpc_info[vpc.id]['is_default'] = vpc.is_default
        vpc_info[vpc.id]['cidr_block'] = vpc.cidr_block
        acls = vpc_connection.get_all_network_acls(filters ={"vpc_id": vpc.id})
        vpc_info[vpc.id]['network_acls'] = {}
        for acl in acls:
            manage_dictionary(vpc_info[vpc.id]['network_acls'], acl.id, {})
            vpc_info[vpc.id]['network_acls'][acl.id]['default'] = acl.default
            vpc_info[vpc.id]['network_acls'][acl.id]['inbound_network_acls'] = get_network_acl_entries(acl.network_acl_entries, "false")
            vpc_info[vpc.id]['network_acls'][acl.id]['outbound_network_acls'] = get_network_acl_entries(acl.network_acl_entries, "true")
        manage_dictionary(vpc_info[vpc.id], 'instances', {})
        count = update_status(count, total, 'VPC')
    close_status(count, total, 'VPC')
    return vpc_info

def get_security_groups_info(ec2_connection, vpc_info):
    groups = ec2_connection.get_all_security_groups()
    count, total = init_status(groups, 'Security groups')
    for group in groups:
        vpc_id = group.vpc_id if group.vpc_id else 'no-vpc'
        manage_dictionary(vpc_info, vpc_id, {})
        # h4ck : data redundancy because I can't call ../@key in Handlebars
        vpc_info[vpc_id]['id'] = vpc_id
        manage_dictionary(vpc_info[vpc_id], 'security_groups', {})
        manage_dictionary(vpc_info[vpc_id]['security_groups'], group.id, {})
        # Append the new security group to the return list
        vpc_info[vpc_id]['security_groups'][group.id] = parse_security_group(group)
        count = update_status(count, total, 'Security groups')
    close_status(count, total, 'Security groups')

def parse_security_group(group):
    security_group = {}
    security_group['name'] = group.name
    security_group['id'] = group.id
    security_group['description'] = group.description
    security_group['owner_id'] = group.owner_id
    security_group = manage_dictionary(security_group, 'running-instances', [])
    security_group = manage_dictionary(security_group, 'stopped-instances', [])
    security_group['rules_ingress'] = parse_security_group_rules(group.rules)
    security_group['rules_egress'] = parse_security_group_rules(group.rules_egress)
    # Save all instances associated with this group
    for i in group.instances():
        if i.state == 'running':
            security_group['running-instances'].append(i.id)
        else:
            security_group['stopped-instances'].append(i.id)
    return security_group

def parse_security_group_rules(rules):
    protocols = {}
    for rule in rules:
        ip_protocol = rule.ip_protocol.upper()
        if ip_protocol == '-1':
            ip_protocol = 'ALL'
        protocols = manage_dictionary(protocols, ip_protocol, {})
        protocols[ip_protocol] = manage_dictionary(protocols[ip_protocol], 'rules', [])
        protocols[ip_protocol]['name'] = ip_protocol
        acl = {}
        acl['grants'] = {}
        # Save grants, values are either a CIDR or an EC2 security group
        for grant in rule.grants:
            if grant.cidr_ip:
                manage_dictionary(acl['grants'], 'cidrs', [])
                acl['grants']['cidrs'].append(grant.cidr_ip)
            else:
                manage_dictionary(acl['grants'], 'security_groups', [])
                acl['grants']['security_groups'].append(grant.groupId) # '%s (%s)' % (grant.name, grant.groupId))
        # Save the port (single port or range)
        if ip_protocol == 'ICMP':
            acl['ports'] = 'N/A'
        elif rule.from_port == rule.to_port:
            if not rule.from_port:
                acl['ports'] = 'All'
            else:
                acl['ports'] = rule.from_port
        else:
            acl['ports'] = '%s-%s' % (rule.from_port, rule.to_port)
        # Save the new rule
        protocols[ip_protocol]['rules'].append(acl)
    return protocols
