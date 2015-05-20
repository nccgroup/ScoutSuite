#!/usr/bin/env python2

# Import AWS Utils
from AWSUtils.utils import *
from AWSUtils.utils_ec2 import *
from AWSUtils.utils_vpc import *
from AWSUtils.protocols_dict import *

# Import Scout2 tools
from AWSScout2.utils import *
from AWSScout2.utils_ec2 import *
from AWSScout2.filters import *
from AWSScout2.findings import *

# Import third-party packages
import boto
from boto import ec2
from boto import vpc
from boto.ec2 import elb


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


########################################
##### EC2 fetch functions
########################################

def get_ec2_info(key_id, secret, session_token, fetch_ec2_gov):
    ec2_info = {}
    ec2_info['regions'] = {}
    # Build region list for each EC2 entities and VPC
    ec2_params = {}
    ec2_params['ec2_regions'] = build_region_list(boto.ec2.regions(), include_gov = fetch_ec2_gov)
    ec2_params['elb_regions'] = build_region_list(boto.ec2.elb.regions(), include_gov = fetch_ec2_gov)
    ec2_params['vpc_regions'] = build_region_list(boto.vpc.regions(), include_gov = fetch_ec2_gov)
    all_regions = set(ec2_params['ec2_regions'] + ec2_params['elb_regions'] + ec2_params['vpc_regions'])
    for region in all_regions:
        ec2_info['regions'][region] = {}
        ec2_info['regions'][region]['name'] = region
    print 'Fetching EC2 data...'
    formatted_status('region', 'Elastic LBs', 'Elastic IPs', 'VPCs', 'Sec. Groups', 'Instances', True)
    ec2_targets = ['elastic_ips', 'elbs', 'vpcs', 'security_groups', 'instances']
    for region in all_regions:
         status['region_name'] = region
         thread_work((key_id, secret, session_token), ec2_info['regions'][region], ec2_targets, thread_region, service_params = ec2_params)
         show_status()
    return ec2_info

def get_elastic_ip_info(ec2_connection, q, params):
    while True:
        try:
            region_info, eip = q.get()
            ip = eip.public_ip
            manage_dictionary(region_info['elastic_ips'], ip, {})
            for key in ['instance_id', 'domain', 'allocation_id', 'association_id', 'network_interface_id', 'network_interface_owner_id', 'private_ip_address']:
                region_info['elastic_ips'][ip][key] = eip.__dict__[key]
            show_status(region_info, 'elastic_ips', False)
        except Exception, e:
            printException(e)
            pass
        finally:
            q.task_done()

def get_elastic_ips_info(ec2_connection, region_info):
    eips = ec2_connection.get_all_addresses()
    count = len(eips)
    if count > 0:
        region_info['elastic_ips_count'] = count
        manage_dictionary(region_info, 'elastic_ips', {})
        show_status(region_info, 'elastic_ips', False)
        thread_work(ec2_connection, region_info, eips, get_elastic_ip_info, None, num_threads = 5)
    else:
        region_info['elastic_ips_count'] = 0
    show_status(region_info, 'elastic_ips', False)

def get_elb_info(elb_connection, q, params):
    while True:
        try:
            region_info, lb = q.get()
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
        except Exception, e:
            printException(e)
            pass
        finally:
            q.task_done()

def get_elbs_info(elb_connection, region_info):
    elbs = elb_connection.get_all_load_balancers()
    region_info['elbs_count'] = len(elbs)
    show_status(region_info, 'elbs', False)
    thread_work(elb_connection, region_info, elbs, get_elb_info, num_threads = 5)
    show_status(region_info, 'elbs', False)

def get_instance_info(ec2_connection, q, paramas):
    while True:
        try:
            region_info, (i, reservation) = q.get()
            vpc_info = region_info['vpcs']
            vpc_id = i.vpc_id if i.vpc_id else 'no-vpc'
            manage_vpc(vpc_info, vpc_id)
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
            read_tags(vpc_info[vpc_id]['instances'][i.id], i)
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
            show_status(vpc_info, 'instances', False)
        except Exception, e:
            printException(e)
            pass
        finally:
            q.task_done()

def get_instances_info(ec2_connection, region_info):
    instances = []
    reservations = ec2_connection.get_all_reservations()
    for reservation in reservations:
        for i in reservation.instances:
            instances.append((i, reservation))
    region_info['instances_count'] = len(instances)
    show_status(region_info, ['vpcs', 'instances'], False)
    thread_work(ec2_connection, region_info, instances, get_instance_info, None, num_threads = 10)
    show_status(region_info, ['vpcs', 'instances'], False)

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

def get_vpc_info(vpc_connection, q, params):
    while True:
        try:
            region_info, vpc = q.get()
            manage_dictionary(region_info, 'vpcs', {})
            manage_dictionary(region_info['vpcs'], vpc.id, {})
            vpc_info = region_info['vpcs'][vpc.id]
            # h4ck : data redundancy because I can't call ../@key in Handlebars
            vpc_info['id'] = vpc.id
            vpc_info['state'] = vpc.state
            vpc_info['is_default'] = vpc.is_default
            vpc_info['cidr_block'] = vpc.cidr_block
            read_tags(vpc_info, vpc)
            acls = vpc_connection.get_all_network_acls(filters ={"vpc_id": vpc.id})
            vpc_info['network_acls'] = {}
            for acl in acls:
                manage_dictionary(vpc_info['network_acls'], acl.id, {})
                vpc_info['network_acls'][acl.id]['default'] = acl.default
                vpc_info['network_acls'][acl.id]['inbound_network_acls'] = get_network_acl_entries(acl.network_acl_entries, "false")
                vpc_info['network_acls'][acl.id]['outbound_network_acls'] = get_network_acl_entries(acl.network_acl_entries, "true")
            manage_dictionary(vpc_info, 'instances', {})
            show_status(region_info, 'vpcs', False, True)
        except Exception, e:
            printException(e)
            pass
        finally:
            q.task_done()

def get_vpcs_info(vpc_connection, region_info):
    vpcs = vpc_connection.get_all_vpcs()
    region_info['vpcs_count'] = len(vpcs)
    show_status(region_info, 'vpcs', False, True)
    thread_work(vpc_connection, region_info, vpcs, get_vpc_info, num_threads = 5)
    show_status(region_info, 'vpcs', False, True)

def get_security_group_info(ec2_connection, q, params):
    while True:
        try:
            region_info, group = q.get()
            vpc_info = region_info['vpcs']
            vpc_id = group.vpc_id if group.vpc_id else 'no-vpc'
            manage_vpc(vpc_info, vpc_id)
            manage_dictionary(vpc_info[vpc_id], 'security_groups', {})
            manage_dictionary(vpc_info[vpc_id]['security_groups'], group.id, {})
            # Append the new security group to the return list
            vpc_info[vpc_id]['security_groups'][group.id] = parse_security_group(group)
            show_status(vpc_info, 'security_groups', False)
        except Exception, e:
            printException(e)
            pass
        finally:
            q.task_done()

def get_security_groups_info(ec2_connection, region_info):
    groups = ec2_connection.get_all_security_groups()
    region_info['security_groups_count' ] = len(groups)
    show_status(region_info, ['vpcs', 'security_groups'], False)    
    thread_work(ec2_connection, region_info, groups, get_security_group_info, num_threads = 10)
    show_status(region_info, ['vpcs', 'security_groups'], False)

def manage_vpc(vpc_info, vpc_id):
    manage_dictionary(vpc_info, vpc_id, {})
    vpc_info[vpc_id]['id'] = vpc_id
    if vpc_id == 'no-vpc':
        vpc_info[vpc_id]['name'] = 'EC2 Classic'
    elif not 'name' in vpc_info[vpc_id]:
        vpc_info[vpc_id]['name'] = vpc_id

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

def read_tags(local, remote):
    if 'Name' in remote.tags and remote.tags['Name'] != '':
        local['name'] = remote.tags['Name']
    else:
        local['name'] = remote.id

status = {}
status['region_name'] = ''
status['elastic_ips'] = 0
status['elbs'] = 0
status['vpcs'] = 0
status['security_groups'] = 0
status['instances'] = 0
def show_status(info = None, entities = None, newline = True, count_self = False):
    if entities:
        subset = info
        if type(entities) == list:
            tmp = entities.pop()
            for e in entities:
                subset = subset[e]
            entities = tmp
        current = 0
        if entities in subset:
            current = len(subset[entities])
        elif count_self == True:
            current = len(subset)   
        elif type(subset) == dict:
            for key in subset:
                if type(subset[key]) == dict and entities in subset[key]:
                    current = current + len(subset[key][entities])
        count = entities + '_count'
        status[entities] = '%d/%d' % (current, info[count]) if count in info else '%d' % current
    formatted_status(status['region_name'], status['elbs'], status['elastic_ips'], status['vpcs'], status['security_groups'], status['instances'], newline)

def formatted_status(region, elbs, eips, vpcs, sgs, instances, newline = False):
    sys.stdout.write('\r{:>20} {:>13} {:>13} {:>13} {:>13} {:>13}'.format(region, elbs, eips, vpcs, sgs, instances))
    sys.stdout.flush()
    if newline:
        sys.stdout.write('\n')    

def thread_region(connection_info, q, ec2_params):
    key_id, secret, session_token = connection_info
    while True:
        try:
            region_info, target = q.get()
            if target == 'elastic_ips':
                if region_info['name'] in ec2_params['ec2_regions']:
                    ec2_connection = connect_ec2(key_id, secret, session_token, region_info['name'])
                    get_elastic_ips_info(ec2_connection, region_info)
            elif target == 'elbs':
                if region_info['name'] in ec2_params['elb_regions']:
                    elb_connection = connect_elb(key_id, secret, session_token, region_info['name'])
                    get_elbs_info(elb_connection, region_info)
            elif target == 'vpcs':
                if region_info['name'] in ec2_params['vpc_regions']:
                    vpc_connection = connect_vpc(key_id, secret, session_token, region_info['name'])
                    manage_dictionary(region_info, 'vpcs', {})
                    get_vpcs_info(vpc_connection, region_info)
            elif target == 'security_groups':
                if region_info['name'] in ec2_params['ec2_regions']:
                    ec2_connection = connect_ec2(key_id, secret, session_token, region_info['name'])
                    manage_dictionary(region_info, 'vpcs', {})
                    get_security_groups_info(ec2_connection, region_info)
            elif target == 'instances':
                if region_info['name'] in ec2_params['ec2_regions']:
                    ec2_connection = connect_ec2(key_id, secret, session_token, region_info['name'])
                    manage_dictionary(region_info, 'vpcs', {})
                    get_instances_info(ec2_connection, region_info)
            else:
                print 'Error'       
        except Exception, e:
            printException(e)
            pass
        finally:
            q.task_done()
