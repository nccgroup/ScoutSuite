#!/usr/bin/env python2

# Import AWS Scout2 tools
from AWSScout2.utils import *
from AWSScout2.protocols_dict import *


########################################
##### VPC functions
########################################

def analyze_vpc_config(vpcs, force_write):
    print 'Analyzing vpc data...'
    vpc_config = {"vpcs": vpcs}

def get_vpc_info(vpc_connection):
    vpc_info = {}
    vpcs = vpc_connection.get_all_vpcs()
    count, total = init_status(vpcs)
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
    return vpc_info

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
