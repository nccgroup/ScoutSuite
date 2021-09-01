from ScoutSuite.providers.aws.resources.base import AWSResources
from ScoutSuite.providers.aws.facade.base import AWSFacade
from ScoutSuite.providers.aws.utils import format_arn
from ScoutSuite.utils import manage_dictionary
from ScoutSuite.core.fs import load_data


class SecurityGroups(AWSResources):
    icmp_message_types_dict = load_data('icmp_message_types.json', 'icmp_message_types')

    def __init__(self, facade: AWSFacade, region: str, vpc: str):
        super().__init__(facade)
        self.region = region
        self.vpc = vpc
        self.partition = facade.partition
        self.service = 'ec2'
        self.resource_type = 'security-group'

    async def fetch_all(self):
        raw_security_groups = await self.facade.ec2.get_security_groups(self.region, self.vpc)
        for raw_security_groups in raw_security_groups:
            name, resource = self._parse_security_group(raw_security_groups)
            self[name] = resource

    def _parse_security_group(self, raw_security_group):
        security_group = {}
        security_group['name'] = raw_security_group['GroupName']
        security_group['id'] = raw_security_group['GroupId']
        security_group['arn'] = format_arn(self.partition, self.service, self.region, raw_security_group.get('OwnerId'), raw_security_group.get('GroupId'), self.resource_type)
        security_group['description'] = raw_security_group['Description']
        security_group['owner_id'] = raw_security_group['OwnerId']

        if 'Tags' in raw_security_group:
            security_group['tags'] = {x['Key']: x['Value'] for x in raw_security_group['Tags']}

        security_group['rules'] = {'ingress': {}, 'egress': {}}
        ingress_protocols, ingress_rules_count = self._parse_security_group_rules(
            raw_security_group['IpPermissions'])
        security_group['rules']['ingress']['protocols'] = ingress_protocols
        security_group['rules']['ingress']['count'] = ingress_rules_count

        egress_protocols, egress_rules_count = self._parse_security_group_rules(
            raw_security_group['IpPermissionsEgress'])
        security_group['rules']['egress']['protocols'] = egress_protocols
        security_group['rules']['egress']['count'] = egress_rules_count

        security_group['is_default_configuration'] = \
            self._has_default_egress_rule(raw_security_group['IpPermissionsEgress']) and \
            self._has_default_ingress_rule(raw_security_group['IpPermissions'], raw_security_group['GroupId'])

        return security_group['id'], security_group

    def _has_default_egress_rule(self, rule_list):
        for rule in rule_list:
            if rule['IpProtocol'] == '-1':
                for ip_range in rule['IpRanges']:
                    if ip_range['CidrIp'] == '0.0.0.0/0':
                        return True
        return False

    def _has_default_ingress_rule(self, rule_list, group_id):
        for rule in rule_list:
            if rule['IpProtocol'] == '-1':
                for source_group in rule['UserIdGroupPairs']:
                    if source_group['GroupId'] == group_id:
                        return True
        return False

    def _parse_security_group_rules(self, rules):
        protocols = {}
        rules_count = 0
        for rule in rules:
            ip_protocol = rule['IpProtocol'].upper()
            if ip_protocol == '-1':
                ip_protocol = 'ALL'
            protocols = manage_dictionary(protocols, ip_protocol, {})
            protocols[ip_protocol] = manage_dictionary(
                protocols[ip_protocol], 'ports', {})

            # Save the port (single port or range)
            port_value = '1-65535'
            if 'FromPort' in rule and 'ToPort' in rule:
                if ip_protocol == 'ICMP':
                    # FromPort with ICMP is the type of message
                    port_value = self.icmp_message_types_dict[str(
                        rule['FromPort'])]
                elif rule['FromPort'] == rule['ToPort']:
                    port_value = str(rule['FromPort'])
                else:
                    port_value = '{}-{}'.format(rule['FromPort'], rule['ToPort'])
            manage_dictionary(protocols[ip_protocol]['ports'], port_value, {})

            # Save grants, values are either a CIDR or an EC2 security group
            for grant in rule['UserIdGroupPairs']:
                manage_dictionary(
                    protocols[ip_protocol]['ports'][port_value], 'security_groups', [])
                protocols[ip_protocol]['ports'][port_value]['security_groups'].append(
                    grant)
                rules_count = rules_count + 1
            for grant in rule['IpRanges']:
                manage_dictionary(
                    protocols[ip_protocol]['ports'][port_value], 'cidrs', [])
                protocols[ip_protocol]['ports'][port_value]['cidrs'].append(
                    {'CIDR': grant['CidrIp']})
                rules_count = rules_count + 1

            # IPv6
            for grant in rule['Ipv6Ranges']:
                manage_dictionary(
                    protocols[ip_protocol]['ports'][port_value], 'cidrs', [])
                protocols[ip_protocol]['ports'][port_value]['cidrs'].append(
                    {'CIDR': grant['CidrIpv6']})
                rules_count = rules_count + 1

        return protocols, rules_count
