from ScoutSuite.providers.osc.resources.base import OSCResources
from ScoutSuite.providers.osc.facade.base import OSCFacade
from ScoutSuite.utils import manage_dictionary

import logging

class SecurityGroups(OSCResources):
    def __init__(self, facade: OSCFacade, region: str, vpc: str = None):
        super(SecurityGroups, self).__init__(facade)
        self.region = region
        self.vpc = vpc

    async def fetch_all(self):
        try:
            raw_security_groups = await self.facade.api.get_security_groups(self.region)
            for raw_security_group in raw_security_groups:
                name, resource = self._parse_security_group(raw_security_group)
                self[name] = resource
        except Exception as e:
            logging.getLogger("scout").critical(f"OSC ::: SecurityGroups _fecth_all() Exception {e}\n\n\n")

    def _parse_security_group(self, raw_security_group):
        security_group = {}
        security_group['name'] = raw_security_group['SecurityGroupName']
        security_group['id'] = raw_security_group['SecurityGroupId']
        security_group['description'] = raw_security_group['Description']
        security_group['owner_id'] = raw_security_group['AccountId']

        if 'Tags' in raw_security_group:
            pass # TODO
        security_group['rules'] = {'ingress': {}, 'egress': {}}
        ingress_protocols, ingress_rules_count = self._parse_security_group_rules(
            raw_security_group['InboundRules'])
        security_group['rules']['ingress']['protocols'] = ingress_protocols
        security_group['rules']['ingress']['count'] = ingress_rules_count
        egress_protocols, egress_rules_count = self._parse_security_group_rules(
            raw_security_group['OutboundRules'])
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
            port_value = '1-65535'
            if 'FromPort' in rule and 'ToPort' in rule:
                if ip_protocol == 'ICMP':
                    # FromPort with ICMP is the type of message
                    # port_value = self.icmp_message_types_dict[str(
                    #     rule['FromPort'])]
                    # TODO
                    pass
                elif rule['FromPort'] == rule['ToPort']:
                    port_value = str(rule['FromPort'])
                else:
                    port_value = '%s-%s' % (rule['FromPort'], rule['ToPort'])
            manage_dictionary(protocols[ip_protocol]['ports'], port_value, {})

            security_groups_members = []
            if 'SecurityGroupsMembers' in rule:
                security_groups_members = rule['SecurityGroupsMembers']
            account_id = "EMPTY"
            if "AccountId" in security_groups_members:
                account_id = security_groups_members["AccountId"]
            protocols = manage_dictionary(protocols, account_id, {})
            protocols[account_id] = manage_dictionary(protocols[account_id], 'users', {})
            owner_id = "NO USERS"
            for member in security_groups_members:
                if "AccountId" in member:
                    owner_id = member["AccountId"]
                rules_count = rules_count + 1
            manage_dictionary(protocols[account_id]['users'], owner_id, {})

            # Save grants, values are either a CIDR or an EC2 security group
            # TODO If Ouscale has something equivalent
            # for grant in rule['UserIdGroupPairs']:
            #     manage_dictionary(
            #         protocols[ip_protocol]['ports'][port_value], 'security_groups', [])
            #     protocols[ip_protocol]['ports'][port_value]['security_groups'].append(
            #         grant)
            #     rules_count = rules_count + 1
            # for grant in rule['IpRanges']:
            #     manage_dictionary(
            #         protocols[ip_protocol]['ports'][port_value], 'cidrs', [])
            #     protocols[ip_protocol]['ports'][port_value]['cidrs'].append(
            #         {'CIDR': grant['CidrIp']})
            #     rules_count = rules_count + 1

            # IPv6
            # TODO If Outscale has something equivalent
            # for grant in rule['Ipv6Ranges']:
            #     manage_dictionary(
            #         protocols[ip_protocol]['ports'][port_value], 'cidrs', [])
            #     protocols[ip_protocol]['ports'][port_value]['cidrs'].append(
            #         {'CIDR': grant['CidrIpv6']})
            #     rules_count = rules_count + 1

        return protocols, rules_count
