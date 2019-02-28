from ScoutSuite.providers.aws.resources.resources import AWSSimpleResources
from ScoutSuite.providers.aws.facade.facade import AWSFacade
from opinel.utils.aws import get_name
from ScoutSuite.providers.aws.utils import ec2_classic, get_keys
from opinel.utils.globals import manage_dictionary
from opinel.utils.fs import load_data


class SecurityGroups(AWSSimpleResources):
    icmp_message_types_dict = load_data('icmp_message_types.json', 'icmp_message_types')

    async def get_resources_from_api(self):
        return self.facade.ec2.get_security_groups(self.scope['region'], self.scope['vpc'])

    def parse_resource(self, raw_security_group):
        security_group = {}
        security_group['name'] = raw_security_group['GroupName']
        security_group['id'] = raw_security_group['GroupId']
        security_group['description'] = raw_security_group['Description']
        security_group['owner_id'] = raw_security_group['OwnerId']

        security_group['rules'] = {'ingress': {}, 'egress': {}}
        ingress_protocols, ingress_rules_count = self._parse_security_group_rules(
            raw_security_group['IpPermissions'])
        security_group['rules']['ingress']['protocols'] = ingress_protocols
        security_group['rules']['ingress']['count'] = ingress_rules_count

        egress_protocols, egress_rules_count = self._parse_security_group_rules(
            raw_security_group['IpPermissionsEgress'])
        security_group['rules']['egress']['protocols'] = egress_protocols
        security_group['rules']['egress']['count'] = egress_rules_count
        return security_group['id'], security_group

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
            port_value = 'N/A'
            if 'FromPort' in rule and 'ToPort' in rule:
                if ip_protocol == 'ICMP':
                    # FromPort with ICMP is the type of message
                    port_value = self.icmp_message_types_dict[str(
                        rule['FromPort'])]
                elif rule['FromPort'] == rule['ToPort']:
                    port_value = str(rule['FromPort'])
                else:
                    port_value = '%s-%s' % (rule['FromPort'], rule['ToPort'])
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
