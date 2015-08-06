from AWSScout2.finding import *

# Import stock packages
import json
import re

# Import third-party packages
import netaddr

#
# EC2 findings
#
class Ec2Finding(Finding):

    re_port_range = re.compile(r'(\d+)\-(\d+)')
    re_single_port = re.compile(r'(\d+)')

    def __init__(self, description, entity, callback, callback_args, level, questions):
        self.keyword_prefix = 'ec2'
        Finding.__init__(self, description, entity, callback, callback_args, level, questions)
        if callback == 'checkNonEIPwhitelisted':
            # When using a custom ruleset, regions are already parsed
            if type(self.callback_args[0]) == dict:
                public_range = []
                for region in self.callback_args[0]:
                    for cidr in self.callback_args[0][region]:
                        public_range.append(cidr)
                self.callback_args = public_range

    def checkInternetAccessiblePort(self, key, obj):
        method = self.callback_args[0]
        if method == 'whitelist':
            protocol = self.callback_args[1][1]
            check_port = self.callback_args[1][2]
        else:
            protocol = self.callback_args[1]
            check_port = self.callback_args[2]
        if protocol in obj['rules']['ingress']['protocols']:
            for port in obj['rules']['ingress']['protocols'][protocol]['ports']:
                if 'cidrs' in obj['rules']['ingress']['protocols'][protocol]['ports'][port]:
                    for cidr in obj['rules']['ingress']['protocols'][protocol]['ports'][port]['cidrs']:
                        if cidr == '0.0.0.0/0':
                            if method == 'blacklist' and self.portInRange(check_port, port):
                                self.addItem(obj['id'])
                            elif method == 'whitelist':
                                if port not in check_port:
                                    self.addItem(port, obj['id'])

    def checkFirstRule(self, key, unsorted_rules):
        sorted_rules = sorted(unsorted_rules, key=lambda k: k['RuleNumber'])
        first_rule = sorted_rules[0]
        if first_rule['port_range'] == '1-65535' and first_rule['CidrBlock'] == '0.0.0.0/0':
            self.addItem(key)

    def checkNetworkACLs(self, key, obj):
        if 'VpcId' in obj and obj['VpcId'] != ec2_classic:
            if 'network_acls' in obj:
                for acl in obj['network_acls']:
                    self.checkFirstRule(key, obj['network_acls'][acl]['rules'][self.callback_args[0]])
            else:
                self.addItem(key)

    def checkNonEIPwhitelisted(self, key, obj):
        for protocol in obj['rules']['ingress']['protocols']:
            for port in obj['rules']['ingress']['protocols'][protocol]['ports']:
                if 'cidrs' in obj['rules']['ingress']['protocols'][protocol]['ports'][port]:
                    for cidr in obj['rules']['ingress']['protocols'][protocol]['ports'][port]['cidrs']:
                        authorized_cidr = netaddr.IPNetwork(cidr)
                        for ec2_cidr in self.callback_args:
                            ec2_cidr = netaddr.IPNetwork(ec2_cidr)
                            if authorized_cidr in ec2_cidr:
                                # Add all EC2 public IPs, check if we have an EIP is performed later
                                self.addItem(cidr, obj['id'])

    def checkSinglePortOnly(self, key, obj):
        for protocol in obj['rules']['ingress']['protocols']:
            for port in obj['rules']['ingress']['protocols'][protocol]['ports']:
                if self.re_port_range.match(str(port)):
                    # Exception: don't flag if the port range is due to AWS' default config that opens all ports to self 
                    grants = obj['rules']['ingress']['protocols'][protocol]['ports'][port]
                    if not ('security_groups' in grants and len(grants['security_groups']) == 1 and grants['security_groups'][0] == obj['id']):
                        self.addItem(port, obj['id'])

    def checkOpenPort(self, key, obj):
        protocol = self.callback_args[0]
        port = self.callback_args[1]
        if protocol in obj['rules']['ingress']['protocols']:
            for rule_port in obj['rules']['ingress']['protocols'][protocol]['ports']:
                if len(self.callback_args) > 2 and self.callback_args[2] != 'no' and self.callback_args[2] != 'n':
                    if self.portInRange(port, rule_port):
                        self.addItem(obj['id'])
                elif port == rule_port:
                    self.addItem(obj['id'])

    def portInRange(self, port, ports):
        result = self.re_port_range.match(ports)
        if result:
            p1 = int(result.group(1))
            p2 = int(result.group(2))
            if int(port) in range(int(result.group(1)), int(result.group(2))):
                return True
        else:
            result = self.re_single_port.match(ports)
            if result and port == result.group(1):
                return True
        return False

    def checkElbSslPolicy(self, key, obj):
        for l in obj['listeners']:
            if l == '443':
                for pn in obj['listeners'][l]['policy_names']:
                    if pn == 'ELBSecurityPolicy-2014-10':
                        return
                    else:
                        self.addItem(pn, obj['name'])

    def isUnused(self, key, obj):
        if 'used_by' not in obj or len(obj['used_by']) == 0:
            self.addItem(obj['id'])

    def checkTrafficRulesToSelf(self, key, obj):
        for protocol in obj['rules']['ingress']['protocols']:
            for port in obj['rules']['ingress']['protocols'][protocol]['ports']:
                grants = obj['rules']['ingress']['protocols'][protocol]['ports'][port]
                if 'security_groups' in grants:
                    for sg in grants['security_groups']:
                        if sg == obj['id'] and (port == 'All' or port == '0-65535'):
                            self.addItem(obj['id'])
