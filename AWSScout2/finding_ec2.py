#!/usr/bin/env python2

from AWSScout2.finding import *

import json
import netaddr
import re

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
            port = self.callback_args[1][2]
        else:
            protocol = self.callback_args[1]
            port = self.callback_args[2]
        if protocol in obj['rules_ingress']:
            for rule in obj['rules_ingress'][protocol]['rules']:
                if 'cidrs' in rule['grants']:
                    for cidr in rule['grants']['cidrs']:
                        if cidr == '0.0.0.0/0':
                            if method == 'blacklist' and self.portInRange(port, rule['ports']):
                                self.addItem(obj['id'])
                            elif method == 'whitelist':
                                if rule['ports'] not in port:
                                    self.addItem(rule['ports'], obj['id'])

    def checkFirstRule(self, key, unsorted_rules):
        sorted_rules = sorted(unsorted_rules, key=lambda k: k['rule_number'])
        first_rule = sorted_rules[0]
        if first_rule['port_range'] == '1-65535' and first_rule['cidr_block'] == '0.0.0.0/0':
            self.addItem(key)

    def checkNetworkACLs(self, key, obj):
        if obj['id'] != 'no-vpc':
            if 'network_acls' in obj:
                field_name = self.callback_args[0] + '_network_acls'
                for acl in obj['network_acls']:
                    self.checkFirstRule(key, obj['network_acls'][acl][field_name])
            else:
                self.addItem(key)

    def checkNonEIPwhitelisted(self, key, obj):
        for protocol in obj['rules_ingress']:
            for rule in obj['rules_ingress'][protocol]['rules']:
                if 'cidrs' in rule['grants']:
                    for cidr in rule['grants']['cidrs']:
                        authorized_cidr = netaddr.IPNetwork(cidr)
                        for ec2_cidr in self.callback_args:
                            ec2_cidr = netaddr.IPNetwork(ec2_cidr)
                            if authorized_cidr in ec2_cidr:
                                # Add all EC2 public IPs, check if we have an EIP is performed later
                                self.addItem(cidr, obj['id'])

    def checkSinglePortOnly(self, key, obj):
        for protocol in obj['rules_ingress']:
            for rule in obj['rules_ingress'][protocol]['rules']:
                if self.re_port_range.match(str(rule['ports'])):
                    # Exception: don't flag if the port range is due to AWS' default config that opens all ports to self
                    if not ('security_groups' in rule['grants'] and len(rule['grants']['security_groups']) == 1 and rule['grants']['security_groups'][0] == obj['id']):
                        self.addItem(rule['ports'], obj['id'])

    def checkOpenPort(self, key, obj):
        protocol = self.callback_args[0]
        port = self.callback_args[1]
        if protocol in obj['rules_ingress']:
            for rule in obj['rules_ingress'][protocol]['rules']:
                for grant in rule['grants']:
                    if len(self.callback_args) > 2 and self.callback_args[2] != 'no' and self.callback_args[2] != 'n':
                        if self.portInRange(port, rule['ports']):
                            self.addItem(obj['id'])
                    elif port == rule['ports']:
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
        if obj['name'] != 'default' and (len(obj['running-instances']) == 0) and (len(obj['stopped-instances']) == 0):
            self.addItem(obj['id'])

    def checkTrafficRulesToSelf(self, key, obj):
        for protocol in obj['rules_ingress']:
            for rule in obj['rules_ingress'][protocol]['rules']:
                for grant in rule['grants']:
                    if 'security_groups' in rule['grants']:
                        for sg in rule['grants']['security_groups']:
                            if sg == obj['id'] and (rule['ports'] == 'All' or rule['ports'] == '0-65535'):
                                self.addItem(obj['id'])
