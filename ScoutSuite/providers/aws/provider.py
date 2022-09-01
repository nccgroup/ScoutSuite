import copy
import os

from ScoutSuite.core.console import print_error, print_exception, print_warning, print_debug
from ScoutSuite.providers.aws.services import AWSServicesConfig
from ScoutSuite.providers.aws.resources.vpc.base import put_cidr_name
from ScoutSuite.providers.aws.utils import ec2_classic, get_aws_account_id, get_partition_name
from ScoutSuite.providers.base.configs.browser import combine_paths, get_object_at, get_value_at
from ScoutSuite.providers.base.provider import BaseProvider
from ScoutSuite.utils import manage_dictionary


class AWSProvider(BaseProvider):
    """
    Implements provider for AWS
    """

    def __init__(self, profile='default', report_dir=None, timestamp=None, services=None, skipped_services=None,
                 result_format='json', **kwargs):
        services = [] if services is None else services
        skipped_services = [] if skipped_services is None else skipped_services

        self.metadata_path = '%s/metadata.json' % os.path.split(os.path.abspath(__file__))[0]

        self.sg_map = {}
        self.subnet_map = {}

        self.profile = profile
        self.services_config = AWSServicesConfig

        self.provider_code = 'aws'
        self.provider_name = 'Amazon Web Services'
        self.environment = self.profile
        self.result_format = result_format

        self.credentials = kwargs['credentials']

        self.partition = get_partition_name(self.credentials.session)

        self.account_id = get_aws_account_id(self.credentials.session)

        super().__init__(report_dir, timestamp,
                                          services, skipped_services, result_format)

    def get_report_name(self):
        """
        Returns the name of the report using the provider's configuration
        """
        if self.profile:
            return f'aws-{self.profile}'
        elif self.account_id:
            return f'aws-{self.account_id}'
        else:
            return 'aws'

    def preprocessing(self, ip_ranges=None, ip_ranges_name_key=None):
        """
        Tweak the AWS config to match cross-service resources and clean any fetching artifacts

        :param ip_ranges:
        :param ip_ranges_name_key:
        :return: None
        """
        ip_ranges = [] if ip_ranges is None else ip_ranges

        # Various data processing calls
        # Note that order of processing can matter

        # TODO - this should be moved to the `finalize` method of the base resource, as it's not cross-service
        self._map_all_subnets()

        # TODO - this should be moved to the `finalize` method of the base resource, as it's not cross-service
        if 'ec2' in self.service_list:
            self._map_all_sgs()
            self._add_security_group_name_to_ec2_grants()
            self._check_ec2_zone_distribution()
            self._add_last_snapshot_date_to_ec2_volumes()

        if 'ec2' in self.service_list and 'iam' in self.service_list:
            self._match_instances_and_roles()
        
        if 'ec2' in self.service_list and 'vpc' in self.service_list:
            self._match_instances_and_vpcs()
            self._match_instances_and_subnets()
        
        if 'ec2' in self.service_list and 'codebuild' in self.service_list:
            self._update_sg_usage_codebuild()

        if 'awslambda' in self.service_list and 'iam' in self.service_list:
            self._match_lambdas_and_roles()

        if 'elbv2' in self.service_list and 'ec2' in self.service_list:
            self._add_security_group_data_to_elbv2()

        if 's3' in self.service_list and 'iam' in self.service_list:
            self._match_iam_policies_and_buckets()

        # TODO - this should be moved to the `finalize` method of the base resource, as it's not cross-service
        if 'elb' in self.services:
            self._parse_elb_policies()

        if 'emr' in self.service_list and 'ec2' in self.service_list and 'vpc' in self.service_list:
            self._set_emr_vpc_ids()

        self._add_cidr_display_name(ip_ranges, ip_ranges_name_key)

        super().preprocessing()

    def _add_cidr_display_name(self, ip_ranges, ip_ranges_name_key):
        if len(ip_ranges):
            callback_args = {'ip_ranges': ip_ranges,
                             'ip_ranges_name_key': ip_ranges_name_key}
            self._go_to_and_do(self.services['ec2'],
                               ['regions', 'vpcs', 'security_groups', 'rules', 'protocols', 'ports'],
                               ['services', 'ec2'],
                               put_cidr_name,
                               callback_args)

    def _add_security_group_name_to_ec2_grants(self):
        """
        Github issue #24: display the security group names in the list of grants (added here to have ligher JS code)
        """
        self._go_to_and_do(self.services['ec2'],
                           ['regions', 'vpcs', 'security_groups', 'rules', 'protocols', 'ports', 'security_groups'],
                           [],
                           self.add_security_group_name_to_ec2_grants_callback,
                           {'AWSAccountId': self.account_id})

    def _add_security_group_data_to_elbv2(self):
        def check_security_group_rules(lb, index, traffic_type):
            none = 'N/A'
            if traffic_type == 'ingress':
                output = 'valid_inbound_rules'
            elif traffic_type == 'egress':
                output = 'valid_outbound_rules'
            for protocol in lb['security_groups'][index]['rules'][traffic_type]['protocols']:
                for port in lb['security_groups'][index]['rules'][traffic_type]['protocols'][protocol]['ports']:
                    lb['security_groups'][index][output] = True
                    if port not in lb['listeners'] and port != none:
                        lb['security_groups'][index][output] = False

        ec2_config = self.services['ec2']
        elbv2_config = self.services['elbv2']
        for region in elbv2_config['regions']:
            for vpc in elbv2_config['regions'][region]['vpcs']:
                for lb in elbv2_config['regions'][region]['vpcs'][vpc]['lbs']:
                    for i in range(0, len(elbv2_config['regions'][region]['vpcs'][vpc]['lbs'][lb]['security_groups'])):
                        for sg in ec2_config['regions'][region]['vpcs'][vpc]['security_groups']:
                            group_id = elbv2_config['regions'][region]['vpcs'][vpc]['lbs'][lb]['security_groups'][i][
                                'GroupId']
                            if 'GroupId' in elbv2_config['regions'][region]['vpcs'][vpc]['lbs'][lb]['security_groups'][
                                i] and group_id == sg:
                                elbv2_config['regions'][region]['vpcs'][vpc]['lbs'][lb]['security_groups'][i] = \
                                    ec2_config['regions'][region]['vpcs'][vpc]['security_groups'][sg]
                                elbv2_config['regions'][region]['vpcs'][vpc]['lbs'][lb]['security_groups'][i][
                                    'GroupId'] = group_id

                        check_security_group_rules(
                            elbv2_config['regions'][region]['vpcs'][vpc]['lbs'][lb], i, 'ingress')
                        check_security_group_rules(
                            elbv2_config['regions'][region]['vpcs'][vpc]['lbs'][lb], i, 'egress')

    def _check_ec2_zone_distribution(self):
        regions = self.services['ec2']['regions'].values()
        self.services['ec2']['number_of_regions_with_instances'] = sum(r['instances_count'] > 0 for r in regions)

        for regions in self.services['ec2']['regions'].values():
            instances_availability_zones = set()
            for vpcs in regions['vpcs'].values():
                for instance in vpcs['instances'].values():
                    instances_availability_zones.add(instance.get('availability_zone'))
            regions['instances_availability_zones'] = len(instances_availability_zones)

    def _add_last_snapshot_date_to_ec2_volumes(self):
        for region in self.services['ec2']['regions'].values():
            for volumeId, volume in region.get('volumes').items():
                completed_snapshots = [s for s in region['snapshots'].values() if
                                       s['volume_id'] == volumeId and s['state'] == 'completed']
                sorted_snapshots = sorted(
                    completed_snapshots, key=lambda s: s['start_time'], reverse=True)
                volume['LastSnapshotDate'] = sorted_snapshots[0]['start_time'] if len(
                    sorted_snapshots) > 0 else None

    def add_security_group_name_to_ec2_grants_callback(self, current_config, path, current_path, ec2_grant,
                                                       callback_args):
        sg_id = ec2_grant['GroupId']
        if sg_id in current_path:
            target = current_path[:(current_path.index(sg_id) + 1)]
            ec2_grant['GroupName'] = get_value_at(self.services['ec2'], target, 'name')
        elif 'UserId' in ec2_grant and ec2_grant['UserId'] == callback_args['AWSAccountId']:
            if 'VpcId' in ec2_grant:
                target = current_path[:(current_path.index('vpcs') + 1)]
                target.append(ec2_grant['VpcId'])
                target.append('security_groups')
                target.append(sg_id)
            else:
                target = current_path[:(
                        current_path.index('security_groups') + 1)]
                target.append(sg_id)
            ec2_grant['GroupName'] = get_value_at(self.services['ec2'], target, 'name')
        elif 'PeeringStatus' in ec2_grant:
            # Can't infer the name of the SG in the peered account
            pass
        else:
            print_warning('Failed to handle EC2 grant: %s' % ec2_grant)

    def process_network_acls_callback(self, current_config, path, current_path, privateip_id, callback_args):
        # Check if the network ACL allows all traffic from all IP addresses
        self._process_network_acls_check_for_allow_all(
            current_config, 'ingress')
        self._process_network_acls_check_for_allow_all(
            current_config, 'egress')
        # Check if the network ACL only has the default rules
        self._process_network_acls_check_for_aws_default(
            current_config, 'ingress')
        self._process_network_acls_check_for_aws_default(
            current_config, 'egress')

    @staticmethod
    def _process_network_acls_check_for_allow_all(network_acl, direction):
        network_acl['allow_all_%s_traffic' % direction] = 0
        for rule_number in network_acl['rules'][direction]:
            rule = network_acl['rules'][direction][rule_number]
            if rule['RuleAction'] == 'deny':
                # If a deny rule appears before an allow all, do not raise the flag
                break
            if (rule['CidrBlock'] == '0.0.0.0/0') and (rule['RuleAction'] == 'allow') and (
                    rule['port_range'] == '1-65535') and (rule['protocol'] == 'ALL'):
                network_acl['allow_all_%s_traffic' % direction] = rule_number
                break

    @staticmethod
    def _process_network_acls_check_for_aws_default(network_acl, direction):
        if len(network_acl['rules'][direction]) == 2 and int(
                network_acl['allow_all_%s_traffic' % direction]) > 0 and '100' in network_acl['rules'][direction]:
            # Assume it is AWS' default rules because there are 2 rules (100 and 65535) and the first rule allows all
            # traffic
            network_acl['use_default_%s_rules' % direction] = True
        else:
            network_acl['use_default_%s_rules' % direction] = False

    def list_ec2_network_attack_surface_callback(self, current_config, path, current_path, privateip_id, callback_args):
        try:
            manage_dictionary(self.services['ec2'], 'external_attack_surface', {})
            if 'Association' in current_config and current_config['Association']:
                public_ip = current_config['Association']['PublicIp']
                self._security_group_to_attack_surface(self.services['ec2']['external_attack_surface'],
                                                       public_ip, current_path,
                                                       [g['GroupId']
                                                        for g in current_config['Groups']],
                                                       [])
                self._complete_information_on_ec2_attack_surface(current_config, current_path, public_ip)

            # IPv6
            if 'Ipv6Addresses' in current_config and len(current_config['Ipv6Addresses']) > 0:
                for ipv6 in current_config.get('Ipv6Addresses', []):
                    ip = ipv6['Ipv6Address']
                    self._security_group_to_attack_surface(self.services['ec2']['external_attack_surface'],
                                                           ip, current_path,
                                                           [g['GroupId'] for g in current_config['Groups']], [])
                    self._complete_information_on_ec2_attack_surface(current_config, current_path, ip)
        except Exception as e:
            print_exception(f"Error listing EC2 network attack surface: {e}")

    def _complete_information_on_ec2_attack_surface(self, current_config, current_path, public_ip):
        try:
            # Get the EC2 instance info
            ec2_info = self.services
            for p in current_path[1:-3]:
                ec2_info = ec2_info[p]
            # Fill the rest of the attack surface details on that IP
            self.services['ec2']['external_attack_surface'][public_ip]['InstanceName'] = ec2_info.get('name')
            if current_config is not None and 'PublicDnsName' in current_config.get('Association', {}):
                self.services['ec2']['external_attack_surface'][public_ip]['PublicDnsName'] = \
                    current_config.get('Association', {}).get('PublicDnsName')
        except Exception as e:
            print_exception(f"Error completing EC2 network attack surface information: {e}")

    def _map_all_sgs(self):
        sg_map = dict()
        self._go_to_and_do(self.services['ec2'],
                           ['regions', 'vpcs', 'security_groups'],
                           ['services', 'ec2'],
                           self.map_resource,
                           {'map': sg_map})
        self.sg_map = sg_map

    def _map_all_subnets(self):
        subnet_map = dict()
        self._go_to_and_do(self.services['vpc'],
                           ['regions', 'vpcs', 'subnets'],
                           ['services', 'vpc'],
                           self.map_resource,
                           {'map': subnet_map})
        self.subnet_map = subnet_map

    @staticmethod
    def map_resource(current_config, path, current_path, resource_id, callback_args):
        if resource_id not in callback_args['map']:
            callback_args['map'][resource_id] = {'region': current_path[3]}
            if len(current_path) > 5:
                callback_args['map'][resource_id]['vpc_id'] = current_path[5]

    def _match_iam_policies_and_buckets(self):
        s3_info = self.services['s3']
        iam_info = self.services['iam']
        if 'Action' in iam_info['permissions']:
            for action in (x for x in iam_info['permissions']['Action'] if
                           ((x.startswith('s3:') and x != 's3:ListAllMyBuckets') or (x == '*'))):
                for iam_entity in iam_info['permissions']['Action'][action]:
                    if 'Allow' in iam_info['permissions']['Action'][action][iam_entity]:
                        for allowed_iam_entity in iam_info['permissions']['Action'][action][iam_entity]['Allow']:
                            # For resource statements, we can easily rely on the existing permissions structure
                            if 'Resource' in \
                                    iam_info['permissions']['Action'][action][iam_entity]['Allow'][allowed_iam_entity]:
                                for full_path in (x for x in
                                                  iam_info['permissions']['Action'][action][iam_entity]['Allow'][
                                                      allowed_iam_entity]['Resource'] if
                                                  x.startswith('arn:aws:s3:') or x == '*'):
                                    parts = full_path.split('/')
                                    bucket_name = parts[0].split(':')[-1]
                                    self._update_iam_permissions(s3_info, bucket_name, iam_entity, allowed_iam_entity,
                                                                 iam_info['permissions']['Action'][action][iam_entity][
                                                                     'Allow'][allowed_iam_entity]['Resource'][
                                                                     full_path])
                            # For notresource statements, we must fetch the policy document to determine which
                            # buckets are not protected
                            if 'NotResource' in iam_info['permissions']['Action'][action][iam_entity]['Allow'][
                                allowed_iam_entity]:
                                for full_path in (x for x in
                                                  iam_info['permissions']['Action'][action][iam_entity]['Allow'][
                                                      allowed_iam_entity]['NotResource'] if
                                                  x.startswith('arn:aws:s3:') or x == '*'):
                                    for policy_type in ['InlinePolicies', 'ManagedPolicies']:
                                        if policy_type in \
                                                iam_info['permissions']['Action'][action][iam_entity]['Allow'][
                                                    allowed_iam_entity]['NotResource'][full_path]:
                                            for policy in \
                                                    iam_info['permissions']['Action'][action][iam_entity]['Allow'][
                                                        allowed_iam_entity]['NotResource'][full_path][policy_type]:
                                                self._update_bucket_permissions(s3_info, iam_info, action, iam_entity,
                                                                                allowed_iam_entity, full_path,
                                                                                policy_type,
                                                                                policy)

    def _update_bucket_permissions(self, s3_info, iam_info, action, iam_entity, allowed_iam_entity, full_path,
                                   policy_type,
                                   policy_name):
        global policy
        allowed_buckets = []
        # By default, all buckets are allowed
        for bucket_name in s3_info['buckets']:
            allowed_buckets.append(bucket_name)
        if policy_type == 'InlinePolicies':
            policy = iam_info[iam_entity.title(
            )][allowed_iam_entity]['Policies'][policy_name]['PolicyDocument']
        elif policy_type == 'ManagedPolicies':
            policy = iam_info['ManagedPolicies'][policy_name]['PolicyDocument']
        else:
            print_error('Error, found unknown policy type.')
        for statement in policy['Statement']:
            for target_path in statement['NotResource']:
                parts = target_path.split('/')
                bucket_name = parts[0].split(':')[-1]
                path = '/' + '/'.join(parts[1:]) if len(parts) > 1 else '/'
                if (path == '/' or path == '/*') and (bucket_name in allowed_buckets):
                    # Remove bucket from list
                    allowed_buckets.remove(bucket_name)
                elif bucket_name == '*':
                    allowed_buckets = []
        policy_info = {policy_type: {}}
        policy_info[policy_type][policy_name] = \
            iam_info['permissions']['Action'][action][iam_entity]['Allow'][allowed_iam_entity]['NotResource'][
                full_path][
                policy_type][policy_name]
        for bucket_name in allowed_buckets:
            self._update_iam_permissions(
                s3_info, bucket_name, iam_entity, allowed_iam_entity, policy_info)

    def _update_iam_permissions(self, s3_info, bucket_name, iam_entity, allowed_iam_entity, policy_info):
        if 's3' in self.service_list and 'iam' in self.service_list:  # validate both services were included in run
            if bucket_name != '*' and bucket_name in s3_info['buckets']:
                bucket = s3_info['buckets'][bucket_name]
                manage_dictionary(bucket, iam_entity, {})
                manage_dictionary(bucket, iam_entity + '_count', 0)
                if allowed_iam_entity not in bucket[iam_entity]:
                    bucket[iam_entity][allowed_iam_entity] = {}
                    bucket[iam_entity + '_count'] = bucket[iam_entity + '_count'] + 1

                if 'inline_policies' in policy_info:
                    manage_dictionary(
                        bucket[iam_entity][allowed_iam_entity], 'inline_policies', {})
                    bucket[iam_entity][allowed_iam_entity]['inline_policies'].update(
                        policy_info['inline_policies'])
                if 'policies' in policy_info:
                    manage_dictionary(bucket[iam_entity]
                                      [allowed_iam_entity], 'policies', {})
                    bucket[iam_entity][allowed_iam_entity]['policies'].update(
                        policy_info['policies'])
            elif bucket_name == '*':
                for bucket in s3_info['buckets']:
                    self._update_iam_permissions(
                        s3_info, bucket, iam_entity, allowed_iam_entity, policy_info)
            else:
                # Could be an error or cross-account access, ignore
                pass

    def match_network_acls_and_subnets_callback(self, current_config, path, current_path, acl_id, callback_args):
        for association in current_config['Associations']:
            subnet_path = current_path[:-1] + \
                          ['subnets', association['SubnetId']]
            subnet = get_object_at(self, subnet_path)
            subnet['network_acl'] = acl_id

    def _match_instances_and_subnets(self):
        ec2_instances = self._get_ec2_instances_details(['id', 'vpc', 'region', 'SubnetId'])  # fetch all EC2 instances with only required fields
        for instance in ec2_instances.values():
            subnet = self.services['vpc']['regions'][instance['region']]['vpcs'][instance['vpc']]['subnets'][instance['SubnetId']]  # find the subnet reference
            manage_dictionary(subnet, 'instances', [])  # initialize instances list for the subnet (if not already set)
            if instance['id'] not in subnet['instances']:  # if instance is not already mapped to the subnet
                subnet['instances'].append(instance['id'])  # append EC2 instance ID to instance list in subnet

    def _get_ec2_instances_details(self, details=None):
        """
        Fetches a list of EC2 instances 

        :param details [str]:       (Optional) List of details to be included, if not specified, all details will be included
        :return:                    A dictionary of EC2 instances with the specified details
        """
        ec2_instances = {}
        for ec2_region_id, ec2_region_data in self.services['ec2']['regions'].items():
            if ec2_region_data['instances_count'] > 0:
                for region_vpc_id, region_vpc_data in ec2_region_data['vpcs'].items():
                    if region_vpc_data['instances_count'] > 0:
                        for ec2_instance_id, ec2_instance_data in region_vpc_data['instances'].items():
                            ec2_instances[ec2_instance_id] = ec2_instance_data.copy()
                            ec2_instances[ec2_instance_id]['region'] = ec2_region_id
                            ec2_instances[ec2_instance_id]['vpc'] = region_vpc_id
        if details is not None:
            for instance_key in ec2_instances.keys():
                for detail in list(ec2_instances[instance_key].keys()):
                    if detail not in details:
                        ec2_instances[instance_key].pop(detail, None)
        return ec2_instances

    def _match_instances_and_vpcs(self):
        ec2_instances = self._get_ec2_instances_details(['id', 'vpc', 'region'])  # fetch all EC2 instances with only required fields
        for instance in ec2_instances.values():
            vpc = self.services['vpc']['regions'][instance['region']]['vpcs'][instance['vpc']]  # find the VPC reference
            manage_dictionary(vpc, 'instances', [])  # initialize instances list for the VPC (if not already set)
            if instance['id'] not in vpc['instances']:  # if instance is not already mapped to the VPC
                vpc['instances'].append(instance['id'])  # append EC2 instance ID to instance list in VPC

    def _match_instances_and_roles(self):
        if 'ec2' in self.service_list and 'iam' in self.service_list:  # validate both services were included in run
            ec2_config = self.services['ec2']
            iam_config = self.services['iam']
            role_instances = {}
            for r in ec2_config['regions']:
                for v in ec2_config['regions'][r]['vpcs']:
                    if 'instances' in ec2_config['regions'][r]['vpcs'][v]:
                        for i in ec2_config['regions'][r]['vpcs'][v]['instances']:
                            instance_profile = ec2_config['regions'][r]['vpcs'][v]['instances'][i]['IamInstanceProfile']
                            instance_profile_id = instance_profile['Id'] if instance_profile else None
                            if instance_profile_id:
                                manage_dictionary(
                                    role_instances, instance_profile_id, [])
                                role_instances[instance_profile_id].append(i)
            for role_id in iam_config['roles']:
                iam_config['roles'][role_id]['instances_count'] = 0
                for instance_profile_id in iam_config['roles'][role_id]['instance_profiles']:
                    if instance_profile_id in role_instances:
                        iam_config['roles'][role_id]['instance_profiles'][instance_profile_id]['instances'] = \
                            role_instances[instance_profile_id]
                        iam_config['roles'][role_id]['instances_count'] += len(
                            role_instances[instance_profile_id])

    def _match_lambdas_and_roles(self):
        if self.services.get('awslambda') and self.services.get('iam'):
            awslambda_config = self.services['awslambda']
            iam_config = self.services['iam']
            awslambda_funtions = {}
            for r in awslambda_config['regions']:
                for lambda_function in awslambda_config['regions'][r]['functions']:
                    awslambda_function = awslambda_config['regions'][r]['functions'][lambda_function]
                    awslambda_function['region'] = r
                    if awslambda_function['role_arn'] in awslambda_funtions:
                        awslambda_funtions[awslambda_function['role_arn']][awslambda_function['name']] = awslambda_function
                    else:
                        awslambda_funtions[awslambda_function['role_arn']] = {awslambda_function['name']: awslambda_function}
            for role_id in iam_config['roles']:
                iam_config['roles'][role_id]['awslambdas_count'] = 0
                if iam_config['roles'][role_id]['arn'] in awslambda_funtions:
                    iam_config['roles'][role_id]['awslambdas'] = awslambda_funtions[iam_config['roles'][role_id]['arn']]
                    iam_config['roles'][role_id]['awslambdas_count'] = len(awslambda_funtions[iam_config['roles'][role_id]['arn']])

    def process_vpc_peering_connections_callback(self, current_config, path, current_path, pc_id, callback_args):

        # Create a list of peering connection IDs in each VPC
        info = 'AccepterVpcInfo' if current_config['AccepterVpcInfo'][
                                        'OwnerId'] == self.account_id else 'RequesterVpcInfo'
        region = current_path[current_path.index('regions') + 1]
        vpc_id = current_config[info]['VpcId']
        if vpc_id not in self.services['vpc']['regions'][region]['vpcs']:
            region = current_config['AccepterVpcInfo']['Region']

        # handle edge case where the region wasn't included in the execution
        if region in self.services['vpc']['regions']:
            target = self.services['vpc']['regions'][region]['vpcs'][vpc_id]
            manage_dictionary(target, 'peering_connections', [])
            if pc_id not in target['peering_connections']:
                target['peering_connections'].append(pc_id)

        # VPC information for the peer'd VPC
        current_config['peer_info'] = copy.deepcopy(
            current_config['AccepterVpcInfo' if info == 'RequesterVpcInfo' else 'RequesterVpcInfo'])
        if 'PeeringOptions' in current_config['peer_info']:
            current_config['peer_info'].pop('PeeringOptions')
        if hasattr(self, 'organization') and current_config['peer_info']['OwnerId'] in self.organization:
            current_config['peer_info']['name'] = self.organization[current_config['peer_info']['OwnerId']][
                'Name']
        else:
            current_config['peer_info']['name'] = current_config['peer_info']['OwnerId']

    def match_roles_and_cloudformation_stacks_callback(self,
                                                       current_config, path, current_path, stack_id, callback_args):
        try:
            if 'RoleARN' not in current_config:
                return
            role_arn = current_config.pop('RoleARN')
            current_config['iam_role'] = self._get_role_info('arn', role_arn)
        except Exception as e:
            print_exception(f'Unable to match roles and CloudFormation stacks: {e}')

    def match_roles_and_vpc_flowlogs_callback(self, current_config, path, current_path, flowlog_id, callback_args):
        if 'DeliverLogsPermissionArn' not in current_config:
            return
        delivery_role_arn = current_config.pop('DeliverLogsPermissionArn')
        current_config['delivery_role'] = self._get_role_info(
            'arn', delivery_role_arn)

    def _get_role_info(self, attribute_name, attribute_value):
        try:
            iam_role_info = {'name': None, 'id': None}
            for role_id in self.services['iam'].get('roles', []):
                if self.services['iam']['roles'][role_id][attribute_name] == attribute_value:
                    iam_role_info['name'] = self.services['iam']['roles'][role_id]['name']
                    iam_role_info['id'] = role_id
                    break
            return iam_role_info
        except Exception as e:
            print_exception(f'Unable to get role info for attribute {attribute_name} with value {attribute_value}: {e}')

    def match_security_groups_and_resources_callback(self, current_config, path, current_path, resource_id,
                                                     callback_args):
        if 'ec2' in self.service_list:  # validate that the service was included in run
            service = current_path[1]
            original_resource_path = combine_paths(
                copy.deepcopy(current_path), [resource_id])
            resource = get_object_at(self, original_resource_path)
            if 'resource_id_path' not in callback_args:
                resource_type = current_path[-1]
                resource_path = copy.deepcopy(current_path)
                resource_path.append(resource_id)
            else:
                resource_path = combine_paths(copy.deepcopy(
                    current_path), callback_args['resource_id_path'])
                resource_id = resource_path[-1]
                resource_type = resource_path[-2]
            if 'status_path' in callback_args:
                status_path = combine_paths(copy.deepcopy(
                    original_resource_path), callback_args['status_path'])
                obj = get_object_at(self, status_path)
                if obj:
                    resource_status = obj.replace('.', '_')
                else:
                    resource_status = obj
            else:
                resource_status = None
            unknown_vpc_id = True if current_path[4] != 'vpcs' else False
            # Issue 89 & 91 : can instances have no security group?
            try:
                try:
                    sg_attribute = get_object_at(
                        resource, callback_args['sg_list_attribute_name'])
                except Exception as e:
                    return
                if type(sg_attribute) != list:
                    sg_attribute = [sg_attribute]
                for resource_sg in sg_attribute:
                    if type(resource_sg) == dict:
                        sg_id = resource_sg[callback_args['sg_id_attribute_name']]
                    else:
                        sg_id = resource_sg
                    if unknown_vpc_id and sg_id:
                        vpc_id = self.sg_map[sg_id]['vpc_id']
                        sg_base_path = copy.deepcopy(current_path[0:4])
                        sg_base_path[1] = 'ec2'
                        sg_base_path = sg_base_path + \
                                       ['vpcs', vpc_id, 'security_groups']
                    else:
                        sg_base_path = copy.deepcopy(current_path[0:6])
                        sg_base_path[1] = 'ec2'
                        sg_base_path.append('security_groups')
                    sg_path = copy.deepcopy(sg_base_path)
                    sg_path.append(sg_id)
                    sg = get_object_at(self, sg_path)
                    # Add usage information
                    manage_dictionary(sg, 'used_by', {})
                    manage_dictionary(sg['used_by'], service, {})
                    manage_dictionary(sg['used_by'][service], 'resource_type', {})
                    manage_dictionary(sg['used_by'][service]['resource_type'], resource_type, {
                    } if resource_status else [])
                    if resource_status:
                        manage_dictionary(
                            sg['used_by'][service]['resource_type'][resource_type], resource_status, [])
                        if resource_id not in sg['used_by'][service]['resource_type'][resource_type][resource_status]:
                            sg['used_by'][service]['resource_type'][resource_type][resource_status].append(
                                {'id': resource_id, 'name': resource['name']})
                    else:
                        sg['used_by'][service]['resource_type'][resource_type].append(
                            {'id': resource_id, 'name': resource['name']})
            except Exception as e:
                if resource_type == 'elbs' and current_path[5] == ec2_classic:
                    pass
                elif not self.services['ec2']:  # service not included in run
                    pass
                elif not str(e):
                    print_exception(f'Failed to parse {resource_type}')
                else:
                    print_exception(f'Failed to parse {resource_type}: {e}')

    def _set_emr_vpc_ids(self):
        clear_list = []
        self._go_to_and_do(self.services['emr'],
                           ['regions', 'vpcs'],
                           ['services', 'emr'],
                           self.set_emr_vpc_ids_callback,
                           {'clear_list': clear_list})
        for region in clear_list:
            self.services['emr']['regions'][region]['vpcs'].pop('EMR-UNKNOWN-VPC')

    def set_emr_vpc_ids_callback(self, current_config, path, current_path, vpc_id, callback_args):
        if vpc_id != 'EMR-UNKNOWN-VPC':
            return
        region = current_path[3]
        vpc_id = sg_id = subnet_id = None
        pop_list = []
        for cluster_id in current_config['clusters']:
            cluster = current_config['clusters'][cluster_id]
            if 'EmrManagedMasterSecurityGroup' in cluster['Ec2InstanceAttributes']:
                sg_id = cluster['Ec2InstanceAttributes']['EmrManagedMasterSecurityGroup']
            elif 'RequestedEc2SubnetIds' in cluster['Ec2InstanceAttributes']:
                subnet_id = cluster['Ec2InstanceAttributes']['RequestedEc2SubnetIds']
            else:
                print_warning('Unable to determine VPC id for EMR cluster %s' % str(cluster_id))
                continue
            if sg_id in self.sg_map:
                vpc_id = self.sg_map[sg_id]['vpc_id']
                pop_list.append(cluster_id)
            else:
                sid_found = False
                if subnet_id:
                    for sid in subnet_id:
                        if sid in self.subnet_map:
                            vpc_id = self.subnet_map[sid]['vpc_id']
                            pop_list.append(cluster_id)
                            sid_found = True
                if not sid_found:
                    print_warning('Unable to determine VPC id for %s' % (str(subnet_id) if subnet_id else str(sg_id)))
                    continue
            if vpc_id:
                region_vpcs_config = get_object_at(self, current_path)
                manage_dictionary(region_vpcs_config, vpc_id, {'clusters': {}})
                region_vpcs_config[vpc_id]['clusters'][cluster_id] = cluster
        for cluster_id in pop_list:
            current_config['clusters'].pop(cluster_id)
        if len(current_config['clusters']) == 0:
            callback_args['clear_list'].append(region)

    def sort_vpc_flow_logs_callback(self, current_config, path, current_path, flow_log_id, callback_args):
        attached_resource = current_config['resource_id']
        if attached_resource.startswith('vpc-'):
            vpc_path = combine_paths(
                current_path[0:4], ['vpcs', attached_resource])
            try:
                attached_vpc = get_object_at(self, vpc_path)
            except Exception:
                print_debug(
                    'It appears that the flow log %s is attached to a resource that was previously deleted (%s).' % (
                        flow_log_id, attached_resource))
                return
            manage_dictionary(attached_vpc, 'flow_logs', [])
            if flow_log_id not in attached_vpc['flow_logs']:
                attached_vpc['flow_logs'].append(flow_log_id)
            for subnet_id in attached_vpc['subnets']:
                manage_dictionary(
                    attached_vpc['subnets'][subnet_id], 'flow_logs', [])
                if flow_log_id not in attached_vpc['subnets'][subnet_id]['flow_logs']:
                    attached_vpc['subnets'][subnet_id]['flow_logs'].append(
                        flow_log_id)
        elif attached_resource.startswith('subnet-'):
            subnet_path = combine_paths(current_path[0:4],
                                        ['vpcs', self.subnet_map[attached_resource]['vpc_id'], 'subnets',
                                         attached_resource])
            subnet = get_object_at(self, subnet_path)
            manage_dictionary(subnet, 'flow_logs', [])
            if flow_log_id not in subnet['flow_logs']:
                subnet['flow_logs'].append(flow_log_id)
        else:
            print_warning('Resource %s attached to flow logs is not handled' % attached_resource)

    def get_db_attack_surface(self, current_config, path, current_path, db_id, callback_args):
        service = current_path[1]
        service_config = self.services[service]
        manage_dictionary(service_config, 'external_attack_surface', {})
        if (service == 'redshift' or service == 'rds') and 'PubliclyAccessible' in current_config and current_config[
            'PubliclyAccessible']:
            public_dns = current_config['Endpoint']['Address']
            listeners = [current_config['Endpoint']['Port']]
            security_groups = current_config['VpcSecurityGroups']
            self._security_group_to_attack_surface(service_config['external_attack_surface'], public_dns,
                                                   current_path, [
                                                       g['VpcSecurityGroupId'] for g in security_groups],
                                                   listeners)
        elif 'ConfigurationEndpoint' in current_config:
            # TODO : get the proper addresss
            public_dns = current_config['ConfigurationEndpoint']['Address'].replace(
                '.cfg', '')
            listeners = [current_config['ConfigurationEndpoint']['Port']]
            security_groups = current_config.get('SecurityGroups', {})
            self._security_group_to_attack_surface(service_config['external_attack_surface'], public_dns,
                                                   current_path, [
                                                       g['SecurityGroupId'] for g in security_groups],
                                                   listeners)
            # TODO :: Get Redis endpoint information

    def get_lb_attack_surface(self, current_config, path, current_path, elb_id, callback_args):
        try:
            public_dns = current_config['DNSName']
            elb_config = self.services[current_path[1]]
            manage_dictionary(elb_config, 'external_attack_surface', {})
            if current_path[1] == 'elbv2' and current_config['Type'] == 'network':
                # Network LBs do not have a security group, lookup listeners instead
                manage_dictionary(
                    elb_config['external_attack_surface'], public_dns, {'protocols': {}})
                for listener in current_config['listeners']:
                    protocol = current_config['listeners'][listener]['Protocol']
                    manage_dictionary(elb_config['external_attack_surface'][public_dns]['protocols'], protocol,
                                      {'ports': {}})
                    manage_dictionary(elb_config['external_attack_surface'][public_dns]['protocols'][protocol]['ports'],
                                      listener, {'cidrs': []})
                    elb_config['external_attack_surface'][public_dns]['protocols'][protocol]['ports'][listener][
                        'cidrs'].append({'CIDR': '0.0.0.0/0'})
            elif current_path[1] == 'elbv2' and current_config['Scheme'] == 'internet-facing':
                elb_config['external_attack_surface'][public_dns] = {
                    'protocols': {}}
                security_groups = [g['GroupId']
                                   for g in current_config['security_groups']]
                listeners = []
                for listener in current_config['listeners']:
                    listeners.append(listener)
                self._security_group_to_attack_surface(elb_config['external_attack_surface'], public_dns,
                                                       current_path, security_groups, listeners)
            elif current_config['Scheme'] == 'internet-facing':
                # Classic ELbs do not have a security group, lookup listeners instead
                public_dns = current_config['DNSName']
                manage_dictionary(elb_config['external_attack_surface'], public_dns, {
                    'protocols': {'TCP': {'ports': {}}}})
                for listener in current_config['listeners']:
                    manage_dictionary(elb_config['external_attack_surface'][public_dns]['protocols']['TCP']['ports'],
                                      listener, {'cidrs': []})
                    elb_config['external_attack_surface'][public_dns]['protocols']['TCP']['ports'][listener][
                        'cidrs'].append({'CIDR': '0.0.0.0/0'})
        except Exception as e:
            print_exception(f'Failed to get LB attack surface: {e}')


    def _security_group_to_attack_surface(self, attack_surface_config, public_ip, current_path,
                                          security_groups, listeners=None):
        try:
            listeners = [] if listeners is None else listeners
            manage_dictionary(attack_surface_config, public_ip, {'protocols': {}})
            instance_path = current_path[:-3]
            if 'ec2' in self.service_list:  # validate that the service was included in run
                for sg_id in security_groups:
                    sg_path = copy.deepcopy(current_path[0:6])
                    sg_path[1] = 'ec2'
                    sg_path.append('security_groups')
                    sg_path.append(sg_id)
                    sg_path.append('rules')
                    sg_path.append('ingress')
                    ingress_rules = get_object_at(self, sg_path)
                    for p in ingress_rules['protocols']:
                        for port in ingress_rules['protocols'][p]['ports']:
                            if len(listeners) == 0 and 'cidrs' in ingress_rules['protocols'][p]['ports'][port]:
                                manage_dictionary(
                                    attack_surface_config[public_ip]['protocols'], p, {'ports': {}})
                                manage_dictionary(attack_surface_config[public_ip]['protocols'][p]['ports'], port,
                                                  {'cidrs': []})
                                attack_surface_config[public_ip]['protocols'][p]['ports'][port]['cidrs'] += \
                                    ingress_rules['protocols'][p]['ports'][port]['cidrs']
                            else:
                                ports = port.split('-')
                                if len(ports) > 1:
                                    try:
                                        if port[0]:
                                            port_min = int(ports[0])
                                        else:
                                            port_min = None
                                        if port[1]:
                                            port_max = int(ports[1])
                                        else:
                                            port_max = None
                                    except Exception as e:
                                        port_min = None
                                        port_max = None
                                elif port == 'N/A':
                                    port_min = port_max = None
                                elif port == 'ALL':
                                    port_min = 0
                                    port_max = 65535
                                elif p == 'ICMP':
                                    port_min = port_max = None
                                else:
                                    port_min = port_max = int(port)
                                for listener in listeners:
                                    if (port_min and port_max) and port_min < int(listener) < port_max and \
                                            'cidrs' in ingress_rules['protocols'][p]['ports'][port]:
                                        manage_dictionary(
                                            attack_surface_config[public_ip]['protocols'], p, {'ports': {}})
                                        manage_dictionary(attack_surface_config[public_ip]['protocols'][p]['ports'],
                                                          str(listener), {'cidrs': []})
                                        attack_surface_config[public_ip]['protocols'][p]['ports'][str(listener)]['cidrs'] += \
                                            ingress_rules['protocols'][p]['ports'][port]['cidrs']
        except Exception as e:
            print_exception(f'Failed to match SG to attack surface: {e}')

    def _parse_elb_policies(self):
        self._go_to_and_do(self.services['elb'],
                           ['regions'],
                           [],
                           self.parse_elb_policies_callback,
                           {})

    def parse_elb_policies_callback(self, current_config, path, current_path, region_id, callback_args):
        region_config = get_object_at(self, ['services', 'elb', ] + current_path + [region_id])
        region_config['elb_policies'] = current_config['elb_policies']
        for policy_id in region_config['elb_policies']:
            if region_config['elb_policies'][policy_id]['PolicyTypeName'] != 'SSLNegotiationPolicyType':
                continue
            # protocols, options, ciphers
            policy = region_config['elb_policies'][policy_id]
            protocols = {}
            options = {}
            ciphers = {}
            for attribute in policy['PolicyAttributeDescriptions']:
                if attribute['AttributeName'] in ['Protocol-SSLv3', 'Protocol-TLSv1', 'Protocol-TLSv1.1',
                                                  'Protocol-TLSv1.2']:
                    protocols[attribute['AttributeName']] = attribute['AttributeValue']
                elif attribute['AttributeName'] in ['Server-Defined-Cipher-Order']:
                    options[attribute['AttributeName']] = attribute['AttributeValue']
                elif attribute['AttributeName'] == 'Reference-Security-Policy':
                    policy['reference_security_policy'] = attribute['AttributeValue']
                else:
                    ciphers[attribute['AttributeName']] = attribute['AttributeValue']
                policy['protocols'] = protocols
                policy['options'] = options
                policy['ciphers'] = ciphers

    def _update_sg_usage_codebuild(self):
        try:
            for region in self.services['codebuild']['regions']:
                for codebuild_project in self.services['codebuild']['regions'][region]['build_projects']:
                    if 'vpc' in self.services['codebuild']['regions'][region]['build_projects'][codebuild_project] and 'security_groups' in self.services['codebuild']['regions'][region]['build_projects'][codebuild_project]:
                        cb_project = self.services['codebuild']['regions'][region]['build_projects'][codebuild_project]
                        for cb_project_sg in cb_project['security_groups']:
                            manage_dictionary(self.services['ec2']['regions'][region]['vpcs'][cb_project['vpc']]['security_groups'][cb_project_sg], 'used_by', {'resource_type': {'codebuild_project': []}})
                            self.services['ec2']['regions'][region]['vpcs'][cb_project['vpc']]['security_groups'][cb_project_sg]['used_by']['resource_type']['codebuild_project'].append({
                                'id': cb_project['arn'], 'name': cb_project['name']
                            })
        except Exception as e:
            print_exception(f'Failed to update security group usage for CodeBuild: {e}')
