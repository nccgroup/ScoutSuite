from AWSScout2.finding import *

#
# Redshift findings
#
class RedshiftFinding(Finding):

    def __init__(self, description, entity, callback, callback_args, level, questions):
        self.keyword_prefix = 'redshift'
        Finding.__init__(self, description, entity, callback, callback_args, level, questions)
