# Import opinel
from opinel.utils import *
from opinel.utils_ec2 import *

# Import Scout2 tools
from AWSScout2.utils import *
from AWSScout2.utils_ec2 import *


########################################
##### Globals
########################################
icmp_message_types_dict = load_data('icmp_message_types.json', 'icmp_message_types')
protocols_dict = load_data('protocols.json', 'protocols')


########################################
##### EC2 analysis functions
########################################

def analyze_ec2_config(ec2_info, aws_account_id, force_write):
    try:
        printInfo('Analyzing EC2 config... ', newLine = False)
        # Tweaks
        link_elastic_ips(ec2_info)
        add_security_group_name_to_ec2_grants(ec2_info, aws_account_id)
        # Custom EC2 analysis
#        check_for_elastic_ip(ec2_info)
        list_network_attack_surface(ec2_info, 'attack_surface', 'PublicIpAddress')
        # TODO: make this optional, commented out for now
        # list_network_attack_surface(ec2_info, 'private_attack_surface', 'PrivateIpAddress')
        printInfo('Success')
    except Exception as e:
        printInfo('Error')
        printException(e)

#
# Github issue #24: display the security group names in the list of grants (added here to have ligher JS code)
#
def add_security_group_name_to_ec2_grants(ec2_config, aws_account_id):
    go_to_and_do(ec2_config, None, ['regions', 'vpcs', 'security_groups', 'rules', 'protocols', 'ports', 'security_groups'], [], add_security_group_name_to_ec2_grants_callback, {'AWSAccountId': aws_account_id})
#
# Callback
#
def add_security_group_name_to_ec2_grants_callback(ec2_config, current_config, path, current_path, ec2_grant, callback_args):
    sg_id = ec2_grant['GroupId']
    if sg_id in current_path:
        target = current_path[:(current_path.index(sg_id)+1)]
        ec2_grant['GroupName'] = get_attribute_at(ec2_config, target, 'name')
    elif ec2_grant['UserId'] == callback_args['AWSAccountId']:
        if 'VpcId' in ec2_grant:
            target = current_path[:(current_path.index('vpcs')+1)]
            target.append(ec2_grant['VpcId'])
            target.append('security_groups')
            target.append(sg_id)
        else:
            target = current_path[:(current_path.index('security_groups')+1)]
            target.append(sg_id)
        ec2_grant['GroupName'] = get_attribute_at(ec2_config, target, 'name')

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
# Link EIP with instances (looks like this might be no longer needed with boto3)
#
def link_elastic_ips(ec2_config):
    return
    go_to_and_do(ec2_config, None, ['regions', 'elastic_ips'], None, link_elastic_ips_callback1, {})

def link_elastic_ips_callback1(ec2_config, current_config, path, current_path, elastic_ip, callback_args):
    if not 'id' in current_config:
        return
    instance_id = current_config['id']
    return
    go_to_and_do(ec2_config, None, ['regions', 'vpcs', 'instances'], None, link_elastic_ips_callback2, {'instance_id': instance_id, 'elastic_ip': elastic_ip})

def link_elastic_ips_callback2(ec2_config, current_config, path, current_path, instance_id, callback_args):
    if instance_id == callback_args['instance_id']:
        if not 'PublicIpAddress' in current_config:
            current_config['PublicIpAddress'] = callback_args['elastic_ip']
        elif current_config['PublicIpAddress'] != callback_args['elastic_ip']:
            printInfo('Warning: public IP address exists (%s) for an instance associated with an elastic IP (%s)' % (current_config['PublicIpAddress'], callback_args['elastic_ip']))
            # This can happen... fix it

#
# List the publicly available IPs/Ports
# TODO use go_to_and_do for that, then add elbs as target too
#
def list_network_attack_surface(ec2_info, attack_surface_attribute_name, ip_attribute_name):
    ec2_info[attack_surface_attribute_name] = {}
    for r in ec2_info['regions']:
        for v in ec2_info['regions'][r]['vpcs']:
            if 'instances' in ec2_info['regions'][r]['vpcs'][v]:
                for i in ec2_info['regions'][r]['vpcs'][v]['instances']:
                    instance = ec2_info['regions'][r]['vpcs'][v]['instances'][i]
                    if instance[ip_attribute_name]:
                        ec2_info[attack_surface_attribute_name][instance[ip_attribute_name]] = {}
                        ec2_info[attack_surface_attribute_name][instance[ip_attribute_name]]['protocols'] = {}
                        for isg in instance['security_groups']:
                            sg = copy.deepcopy(ec2_info['regions'][r]['vpcs'][v]['security_groups'][isg['GroupId']])
                            tmp = ec2_info[attack_surface_attribute_name][instance[ip_attribute_name]]
                            for p in ec2_info['regions'][r]['vpcs'][v]['security_groups'][isg['GroupId']]['rules']['ingress']['protocols']:
                                for port in ec2_info['regions'][r]['vpcs'][v]['security_groups'][isg['GroupId']]['rules']['ingress']['protocols'][p]['ports']:
                                    if not 'cidrs' in sg['rules']['ingress']['protocols'][p]['ports'][port]:
                                        sg['rules']['ingress']['protocols'][p]['ports'].pop(port, None)
                                    elif 'security_groups' in ec2_info['regions'][r]['vpcs'][v]['security_groups'][isg['GroupId']]['rules']['ingress']['protocols'][p]['ports'][port]:
                                        sg['rules']['ingress']['protocols'][p]['ports'][port].pop('security_groups', None)
                                if not sg['rules']['ingress']['protocols'][p]['ports']:
                                    sg['rules']['ingress']['protocols'].pop(p)
                            tmp = tmp.update(sg['rules']['ingress'])


########################################
##### EC2 fetch functions
########################################

def get_ec2_info(credentials, service_config, selected_regions, partition_name):
    # Prep regions
    all_regions = build_region_list('ec2', selected_regions, partition_name)
    manage_dictionary(service_config, 'regions', {})
    for region in all_regions:
        manage_dictionary(service_config['regions'], region, {})
        service_config['regions'][region]['name'] = region
    # Fetch VPCs first, then thread on the other objects
    printInfo('Fetching basic VPC information...')
    params = {}
    params['creds'] = credentials
    params['service_config'] = service_config
    thread_work(all_regions, get_vpc_info, params = params)
    # Fetch VPC/EC2 objects
    printInfo('Fetching EC2 and VPC config...')
    ec2_targets = ['elastic_ips', 'elbs', 'flow_logs', 'instances', 'network_acls', 'security_groups', 'subnets']
    formatted_status('region', 'Elastic IPs', 'Elastic LBs', 'Flow Logs', 'Instances', 'Network ACLs', 'Sec. Groups', 'Subnets', True)
    for region in all_regions:
         status['region_name'] = region
         manage_dictionary(service_config['regions'][region], 'vpcs', {})
         params = {}
         params['creds'] = credentials
         params['ec2_client'] = connect_ec2(credentials, region)
         params['region_info'] = service_config['regions'][region]
         thread_work(ec2_targets, thread_region, params = params)
         show_status()
         list_instances_in_security_groups(service_config['regions'][region])

#
# Once all the data has been fetched, iterate through instances and list them 
# Could this be done when all the "used_by" values are set ??? TODO
#
def list_instances_in_security_groups(region_info):
    for vpc in region_info['vpcs']:
        if not 'instances' in region_info['vpcs'][vpc]:
            return
        for instance in region_info['vpcs'][vpc]['instances']:
            state = region_info['vpcs'][vpc]['instances'][instance]['State']['Name']
            for sg in region_info['vpcs'][vpc]['instances'][instance]['security_groups']:
                sg_id = sg['GroupId']
                manage_dictionary(region_info['vpcs'][vpc]['security_groups'][sg_id], 'instances', {})
                manage_dictionary(region_info['vpcs'][vpc]['security_groups'][sg_id]['instances'], state, [])
                region_info['vpcs'][vpc]['security_groups'][sg_id]['instances'][state].append(instance)

#
# Parse and save one EIp
#
def get_elastic_ip_info(q, params):
    ec2_client = params['ec2_client']
    region_info = params['region_info']
    while True:
        try:
            eip = q.get()
            manage_dictionary(region_info['elastic_ips'], eip['PublicIp'], eip)
            show_status(region_info, 'elastic_ips', False)
        except Exception as e:
            printException(e)
        finally:
            q.task_done()

#
# Fetch all EIPs
#
def get_elastic_ips_info(ec2_client, region_info):
    eips = ec2_client.describe_addresses()['Addresses']
    count = len(eips)
    if count > 0:
        region_info['elastic_ips_count'] = count
        manage_dictionary(region_info, 'elastic_ips', {})
        show_status(region_info, 'elastic_ips', False)
        thread_work(eips, get_elastic_ip_info, params = {'ec2_client': ec2_client, 'region_info': region_info}, num_threads = 5)
    else:
        region_info['elastic_ips_count'] = 0
    show_status(region_info, 'elastic_ips', False)

#
# Parse and save one ELB
#
def get_elb_info(q, params):
    elb_client = params['elb_client']
    region_info = params['region_info']
    while True:
        try:
            lb = q.get()
            elb = {}
            elb['name'] = lb.pop('LoadBalancerName')
            vpc_id = lb['VPCId'] if 'VPCId' in lb and lb['VPCId'] else ec2_classic
            for key in ['DNSName', 'CreatedTime', 'AvailabilityZones', 'Subnets', 'Policies', 'Scheme']:
                elb[key] = lb[key] if key in lb else None
            elb['security_groups'] = []
            for sg in lb['SecurityGroups']:
                elb['security_groups'].append({'GroupId': sg})
            manage_dictionary(elb, 'listeners', {})
            for l in lb['ListenerDescriptions']:
                listener = l['Listener']
                manage_dictionary(listener, 'policies', {})
                for policy_name in l['PolicyNames']:
                    manage_dictionary(listener['policies'], policy_name, {})
                elb['listeners'][l['Listener']['LoadBalancerPort']] = listener
            manage_dictionary(elb, 'instances', [])
            for i in lb['Instances']:
                elb['instances'].append(i['InstanceId'])
            # Save
            manage_dictionary(region_info, 'vpcs', {})
            manage_dictionary(region_info['vpcs'], vpc_id, {})
            manage_dictionary(region_info['vpcs'][vpc_id], 'elbs', {})
            manage_dictionary(region_info['vpcs'][vpc_id]['elbs'], get_non_aws_id(elb['name']), elb)
        except Exception as e:
            printException(e)
        finally:
            q.task_done()

#
# Fetch all ELBs
#
def get_elbs_info(elb_client, region_info):
    elbs = elb_client.describe_load_balancers()['LoadBalancerDescriptions']
    region_info['elbs_count'] = len(elbs)
    show_status(region_info, 'elbs', False)
    thread_work(elbs, get_elb_info, params = {'elb_client': elb_client, 'region_info': region_info}, num_threads = 5)
    show_status(region_info, 'elbs', False)

#
# Parse and save one flow log
#
def get_flow_log_info(q, params):
    ec2_client = params['ec2_client']
    region_info = params['region_info']
    while True:
        try:
            fl = q.get()
            fl_id = fl.pop('FlowLogId')
            resource_id = fl.pop('ResourceId')
            if resource_id.startswith('vpc-'):
                manage_dictionary(region_info['vpcs'], resource_id, {})
                manage_dictionary(region_info['vpcs'][resource_id], 'flow_logs', {})
                region_info['vpcs'][resource_id]['flow_logs'][fl_id] = fl
            elif resource_id.startswith('subnet-'):
                # Temporary save within the region, once subnets are fetched too, do an update at the end of the run
                manage_dictionary(region_info, 'subnets', {})
                manage_dictionary(region_info['subnets'], resource_id, {})
                manage_dictionary(region_info['subnets'][resource_id], 'flow_logs', {})
                region_info['subnets'][resource_id]['flow_logs'][fl_id] = fl
            # Status update
            show_status(region_info['vpcs'], 'flow_logs', False)
        except Exception as e:
            printException(e)
        finally:
            q.task_done()

#
# Fetch all flow logs
#
def get_flow_logs_info(ec2_client, region_info):
    flow_logs = handle_truncated_response(ec2_client.describe_flow_logs, {}, ['FlowLogs'])['FlowLogs']
    region_info['flow_logs_count'] = len(flow_logs)
    show_status(region_info['vpcs'], 'flow_logs', False)
    thread_work(flow_logs, get_flow_log_info, params = {'ec2_client': ec2_client, 'region_info': region_info}, num_threads = 5)
    show_status(region_info['vpcs'], 'flow_logs', False)

#
# Parse and save one instance
#
def get_instance_info(q, params):
    ec2_client = params['ec2_client']
    region_info = params['region_info']
    while True:
        try:
            i, reservation_id = q.get()
            # Get instance variables
            instance = {}
            vpc_id = i['VpcId'] if 'VpcId' in i and i['VpcId'] else ec2_classic
            instance['reservation_id'] = reservation_id
            instance['id'] = i['InstanceId']
            get_name(instance, i, 'InstanceId')
            # TODO: use get_keys() here
            for key in ['PublicDnsName', 'PrivateDnsName', 'KeyName', 'LaunchTime', 'PrivateIpAddress', 'PublicIpAddress', 'InstanceType', 'State']:
                instance[key] = i[key] if key in i else None
            if 'IamInstanceProfile' in i:
                instance['iam_instance_profile'] = {}
                get_keys(i['IamInstanceProfile'], instance['iam_instance_profile'], ['Id', 'Arn'])
            manage_dictionary(instance, 'security_groups', [])
            for sg in i['SecurityGroups']:
                instance['security_groups'].append(sg)
            # Save new instance
            manage_vpc(region_info['vpcs'], vpc_id)
            manage_dictionary(region_info['vpcs'][vpc_id], 'instances', {})
            region_info['vpcs'][vpc_id]['instances'][i['InstanceId']] = instance
            # Status update
            show_status(region_info['vpcs'], 'instances', False)
        except Exception as e:
            printException(e)
        finally:
            q.task_done()

#
# Fetch all instances
#
def get_instances_info(ec2_client, region_info):
    instances = []
    reservations = ec2_client.describe_instances()['Reservations']
    for reservation in reservations:
        for i in reservation['Instances']:
            instances.append((i, reservation['ReservationId']))
    region_info['instances_count'] = len(instances)
    show_status(region_info, ['vpcs', 'instances'], False)
    thread_work(instances, get_instance_info, params = {'ec2_client': ec2_client, 'region_info': region_info}, num_threads = 10)
    show_status(region_info, ['vpcs', 'instances'], False)

#
# Parse and save one network ACL
#
def get_network_acl_info(q, params):
    ec2_client = params['ec2_client']
    region_info = params['region_info']
    while True:
        try:
            network_acl = q.get()
            vpc_id = network_acl['VpcId']
            vpc = region_info['vpcs'][vpc_id]
            acl_id = network_acl['NetworkAclId']
            manage_dictionary(vpc['network_acls'], acl_id, {})
            vpc['network_acls'][acl_id] = network_acl
            get_name(vpc['network_acls'][acl_id], network_acl, 'NetworkAclId')
            manage_dictionary(vpc['network_acls'][acl_id], 'rules', {})
            vpc['network_acls'][acl_id]['rules']['ingress'] = get_network_acl_entries(network_acl['Entries'], False)
            vpc['network_acls'][acl_id]['rules']['egress'] = get_network_acl_entries(network_acl['Entries'], True)
            vpc['network_acls'][acl_id].pop('Entries')
            # Status update
            show_status(region_info['network_acls'], 'network_acls', False)
        except Exception as e:
            printException(e)
        finally:
            q.task_done()

#
# Parse one network ACL's entries
#
def get_network_acl_entries(entries, egress):
    acl_list = []
    for entry in entries:
        if entry['Egress'] == egress:
            acl = {}
            for key in ['CidrBlock', 'RuleAction', 'RuleNumber']:
                acl[key] = entry[key]
            acl['protocol'] = protocols_dict[entry['Protocol']]
            if 'PortRange' in entry:
                from_port = entry['PortRange']['From'] if entry['PortRange']['From'] else 1
                to_port = entry['PortRange']['To'] if entry['PortRange']['To'] else 65535
                acl['port_range'] = from_port if from_port == to_port else str(from_port) + '-' + str(to_port)
            else:
                acl['port_range'] = '1-65535'

            acl_list.append(acl)
    return acl_list

#
# Fetch all network ACLs
#
def get_network_acls_info(ec2_client, region_info):
    network_acls = handle_truncated_response(ec2_client.describe_network_acls, {}, ['NetworkAcls'])['NetworkAcls']
    region_info['network_acls'] = {}
    region_info['network_acls_count'] = len(network_acls)
    show_status(region_info['network_acls'], 'network_acls', False)
    thread_work(network_acls, get_network_acl_info, params = {'ec2_client': ec2_client, 'region_info': region_info}, num_threads = 5)
    show_status(region_info['network_acls'], 'network_acls', False)

#
# Fetch all VPCs
# 
def get_vpc_info(q, ec2_params):
    while True:
        try:
            region = q.get()
            region_info = ec2_params['service_config']['regions'][region]
            region_info['vpcs'] = {}
            ec2_client = connect_ec2(ec2_params['creds'], region_info['name'])
            vpcs = ec2_client.describe_vpcs()['Vpcs']
            region_info['vpcs_count'] = len(vpcs)
            for vpc in vpcs:
                vpc_id = vpc['VpcId']
                manage_dictionary(region_info['vpcs'], vpc_id, {})
                get_name(vpc, vpc, 'VpcId')
                manage_vpc(region_info['vpcs'][vpc_id], vpc_id)
                manage_dictionary(region_info['vpcs'][vpc_id], 'instances', {})
                manage_dictionary(region_info['vpcs'][vpc_id], 'network_acls', {})
                manage_dictionary(region_info['vpcs'][vpc_id], 'security_groups', {})

            # By default, create a place holder for EC2-Classic that will be removed in empty at the end of the run
            manage_dictionary(region_info['vpcs'], ec2_classic, {})
        except Exception as e:
            printException(e)
        finally:
            q.task_done()

#
# Parse and save one security group
#
def get_security_group_info(q, params):
    ec2_client = params['ec2_client']
    region_info = params['region_info']
    while True:
        try:
            group = q.get()
            vpc_id = group['VpcId'] if 'VpcId' in group and group['VpcId'] else ec2_classic
            manage_vpc(region_info['vpcs'], vpc_id)
            manage_dictionary(region_info['vpcs'][vpc_id], 'security_groups', {})
            manage_dictionary(region_info['vpcs'][vpc_id]['security_groups'], group['GroupId'], {})
            security_group = {}
            security_group['name'] = group['GroupName']
            security_group['id'] = group['GroupId']
            security_group['description'] = group['Description']
            security_group['owner_id'] = group['OwnerId']
            security_group['rules'] = {'ingress': {}, 'egress': {}}
            security_group['rules']['ingress']['protocols'], security_group['rules']['ingress']['count'] = parse_security_group_rules(group['IpPermissions'])
            security_group['rules']['egress']['protocols'],  security_group['rules']['egress']['count']  = parse_security_group_rules(group['IpPermissionsEgress'])

            region_info['vpcs'][vpc_id]['security_groups'][group['GroupId']] = security_group
            show_status(region_info['vpcs'], 'security_groups', False)
        except Exception as e:
            printException(e)
        finally:
            q.task_done()

#
# Fetch all security groups
#
def get_security_groups_info(ec2_client, region_info):
    security_groups = ec2_client.describe_security_groups()['SecurityGroups']
    region_info['security_groups_count' ] = len(security_groups)
    show_status(region_info, ['vpcs', 'security_groups'], False)
    thread_work(security_groups, get_security_group_info, params = {'ec2_client': ec2_client, 'region_info': region_info}, num_threads = 10)
    show_status(region_info, ['vpcs', 'security_groups'], False)

#
# Ensure name and ID are set
#
def manage_vpc(vpc_info, vpc_id):
    manage_dictionary(vpc_info, vpc_id, {})
    vpc_info[vpc_id]['id'] = vpc_id
    if not 'name' in vpc_info[vpc_id]:
        vpc_info[vpc_id]['name'] = vpc_id

#
# Parse one security group's rules
#
def parse_security_group_rules(rules):
    protocols = {}
    rules_count = 0
    for rule in rules:
        ip_protocol = rule['IpProtocol'].upper()
        if ip_protocol == '-1':
            ip_protocol = 'ALL'
        protocols = manage_dictionary(protocols, ip_protocol, {})
        protocols[ip_protocol] = manage_dictionary(protocols[ip_protocol], 'ports', {})
        # Save the port (single port or range)
        port_value = 'N/A'
        if 'FromPort' in rule and 'ToPort' in rule:
            if ip_protocol == 'ICMP':
                # FromPort with ICMP is the type of message
                port_value = icmp_message_types_dict[str(rule['FromPort'])]
            elif rule['FromPort'] == rule['ToPort']:
                port_value = str(rule['FromPort'])
            else:
                port_value = '%s-%s' % (rule['FromPort'], rule['ToPort'])
        manage_dictionary(protocols[ip_protocol]['ports'], port_value, {})
        # Save grants, values are either a CIDR or an EC2 security group
        for grant in rule['UserIdGroupPairs']:
            manage_dictionary(protocols[ip_protocol]['ports'][port_value], 'security_groups', [])
            protocols[ip_protocol]['ports'][port_value]['security_groups'].append(grant)
            rules_count = rules_count + 1
        for grant in rule['IpRanges']:
            manage_dictionary(protocols[ip_protocol]['ports'][port_value], 'cidrs', [])
            protocols[ip_protocol]['ports'][port_value]['cidrs'].append({'CIDR': grant['CidrIp']})
            rules_count = rules_count + 1
    return protocols, rules_count

#
# Display
#
status = {}
status['region_name'] = ''
status['elastic_ips'] = 0
status['elbs'] = 0
status['flow_logs'] = 0
status['instances'] = 0
status['network_acls'] = 0
status['security_groups'] = 0
status['subnets'] = 0

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
    formatted_status(status['region_name'], status['elastic_ips'], status['elbs'], status['flow_logs'], status['instances'], status['network_acls'], status['security_groups'], status['subnets'], newline)

def formatted_status(region, eips, elbs, flow_logs, instances, network_acls, sgs, subnets, newline = False):
    sys.stdout.write('\r{:>20} {:>13} {:>13} {:>13} {:>13} {:>13} {:>13} {:>13}'.format(region, eips, elbs, flow_logs, instances, network_acls, sgs, subnets))
    sys.stdout.flush()
    if newline:
        sys.stdout.write('\n')

#
# Per-region thread helper
#
def thread_region(q, ec2_params):
    ec2_client = ec2_params['ec2_client']
    region_info = ec2_params['region_info']
    while True:
        try:
            target = q.get()
            if target == 'elastic_ips':
                get_elastic_ips_info(ec2_client, region_info)
            elif target == 'elbs':
                elb_client = connect_elb(ec2_params['creds'], region_info['name'])
                get_elbs_info(elb_client, region_info)
            elif target == 'flow_logs':
                get_flow_logs_info(ec2_client, region_info)
            elif target == 'instances':
                get_instances_info(ec2_client, region_info)
            elif target == 'network_acls':
                get_network_acls_info(ec2_client, region_info)
            elif target == 'security_groups':
                get_security_groups_info(ec2_client, region_info)
            elif target == 'subnets':
                pass
                #get_subnets_info(ec2_client, region_info)
            else:
                printError('Error: %s are not supported yet.' % target)
        except Exception as e:
            printException(e)
        finally:
            q.task_done()
