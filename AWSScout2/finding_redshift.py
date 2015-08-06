from AWSScout2.finding import *

#
# Redshift findings
#
class RedshiftFinding(Finding):

    def __init__(self, description, entity, callback, callback_args, level, questions):
        self.keyword_prefix = 'redshift'
        Finding.__init__(self, description, entity, callback, callback_args, level, questions)

    def checkParameterIsNotTrue(self, key, obj):
        for parameter in obj['parameters']:
            if parameter == self.callback_args[0]:
                if (obj['parameters'][parameter]['value']).lower() != 'true':
                    self.addItem(key)

    def checkSecurityGroupAllowsAll(self, key, obj):
        if 'IPRanges' in obj:
            for IPRange in obj['IPRanges']:
                if IPRange['Status'] == 'authorized' and IPRange['CIDRIP'] == '0.0.0.0/0':
                    self.addItem(key)
