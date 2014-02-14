#!/usr/bin/env python2

from AWSScout2.finding import *

import re

class Ec2Finding(Finding):

    re_port_range = re.compile(r'(\d+)\-(\d+)')
    re_single_port = re.compile(r'(\d+)')

    def __init__(self, description, entity, callback, callback_args, idprefix, level):
        self.keyword_prefix = 'ec2'
        Finding.__init__(self, description, entity, callback, callback_args, idprefix, level)

    def checkInternetAccessiblePort(self, key, obj):
        protocol = self.callback_args[0][1][0].lower()
        method = self.callback_args[0][0]
        port = self.callback_args[0][1][1]
        if protocol in obj['protocols']:
            for rule in obj['protocols'][protocol]['rules']:
                for grant in rule['grants']:
                    if grant == '0.0.0.0/0':
                        if method == 'blacklist' and self.portInRange(port, rule['ports']):
                            self.items.append(obj['id'] + '-' + protocol.upper() + '-' + port + '-' + grant)
                            self.macro_items.append(obj['id'])
                        elif method == 'whitelist':
                            if rule['ports'] not in port:
                                self.items.append(obj['id'] + '-' + protocol.upper() + '-' + rule['ports'] + '-' + grant)
                                self.macro_items.append(obj['id'])

    def checkOpenPort(self, key, obj):
        protocol = self.callback_args[0][0].lower()
        port = self.callback_args[0][1]
        if protocol in obj['protocols']:
            for rule in obj['protocols'][protocol]['rules']:
                for grant in rule['grants']:
                    if self.portInRange(port, rule['ports']):
                        self.items.append(obj['id'] + '-' + protocol.upper() + '-' + port)
                        self.macro_items.append(obj['id'])

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
