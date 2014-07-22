#!/usr/bin/env python2

from AWSScout2.finding import *

import re

class Ec2Finding(Finding):

    re_port_range = re.compile(r'(\d+)\-(\d+)')
    re_single_port = re.compile(r'(\d+)')

    def __init__(self, description, entity, callback, callback_args, level):
        self.keyword_prefix = 'ec2'
        Finding.__init__(self, description, entity, callback, callback_args, level)

    def checkInternetAccessiblePort(self, key, obj):
        method = self.callback_args[0][0]
        if method == 'whitelist':
            protocol = self.callback_args[0][1][1].lower()
            port = self.callback_args[0][1][2]
        else:
            protocol = self.callback_args[0][1].lower()
            port = self.callback_args[0][2]
        if protocol in obj['protocols']:
            for rule in obj['protocols'][protocol]['rules']:
                for grant in rule['grants']:
                    if grant == '0.0.0.0/0':
                        if method == 'blacklist' and self.portInRange(port, rule['ports']):
                            self.addItem(obj['id'])
                        elif method == 'whitelist':
                            if rule['ports'] not in port:
                                self.addItem(obj['id'])

    def checkFirstRule(self, key, unsorted_rules):
        sorted_rules = sorted(unsorted_rules, key=lambda k: k['rule_number'])
        first_rule = sorted_rules[0]
        if first_rule['port_range'] == '1-65535' and first_rule['cidr_block'] == '0.0.0.0/0':
            self.addItem(key)

    def checkNetworkACLs(self, key, obj):
        if 'network_acls' in obj:
            field_name = self.callback_args[0] + '_network_acls'
            for acl in obj['network_acls']:
                self.checkFirstRule(key, obj['network_acls'][acl][field_name])
        else:
            self.addItem(key)

    def checkUnscannableInstanceTypes(self, key, obj):
        if 'instance_type' in obj and self.callback_args:
            instance_type = obj['instance_type']
            if instance_type in self.callback_args[0]:
                self.addItem(key)

    def checkOpenPort(self, key, obj):
        protocol = self.callback_args[0][0].lower()
        port = self.callback_args[0][1]
        if protocol in obj['protocols']:
            for rule in obj['protocols'][protocol]['rules']:
                for grant in rule['grants']:
                    if self.portInRange(port, rule['ports']):
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
                    if pn == 'ELBSecurityPolicy-2014-01':
                        return
                    else:
                        self.addItem(pn, obj['name'])
