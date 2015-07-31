from AWSScout2.filter import *

#
# EC2 filters
#
class Ec2Filter(Filter):

    def __init__(self, description, entity, callback, callback_args):
        self.keyword_prefix = 'ec2'
        Filter.__init__(self, description, entity, callback, callback_args)

    def hasNoRunningInstances(self, key, obj):
        if not 'instances' in obj or not 'running' in obj['instances'] or len(obj['instances']['running']) == 0:
            self.addItem(obj['id'])

    def HasNoCIDRsGrants(self, key, obj):
        if not len(obj['rules']['ingress']['protocols']):
            self.addItem(obj['id'])
            return
        for protocol in obj['rules']['ingress']['protocols']:
            for port in obj['rules']['ingress']['protocols'][protocol]['ports']:
                if not 'cidrs' in obj['rules']['ingress']['protocols'][protocol]['ports'][port]:
                    self.addItem(obj['id'])

    def DoesNotOpenAllPorts(self, key, obj):
        if not len(obj['rules']['ingress']['protocols']):
            self.addItem(obj['id']);
            return
        for protocol in obj['rules']['ingress']['protocols']:
            for port in obj['rules']['ingress']['protocols'][protocol]['ports']:
                if port != '1-65535' and port != 'All':
                    self.addItem(obj['id'])

    def DoesNotHaveAPublicIP(self, key, obj):
        if not obj['PublicIpAddress']:
            self.addItem(obj['InstanceId'])

    def IsOpenToAll(self, key, obj):
        for ip in obj:
            for p in obj[ip]: 
                for port in obj[ip][p]:
                    if 'cidrs' in obj[ip][p][port]:
                        for cidr in obj[ip][p][port]['cidrs']:
                            if cidr == '0.0.0.0/0':
                                self.addItem('%s-%s-%s' % (ip, p, port))
