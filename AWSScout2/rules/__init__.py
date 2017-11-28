# -*- coding: utf-8 -*-

import os

condition_operators = [ 'and', 'or' ]

awsscout2_rules_data_dir  = os.path.join(os.path.dirname(__file__), 'data')
awsscout2_conditions_dir  = os.path.join(awsscout2_rules_data_dir, 'conditions')
awsscout2_filters_dir     = os.path.join(awsscout2_rules_data_dir, 'filters')
awsscout2_findings_dir    = os.path.join(awsscout2_rules_data_dir, 'findings')
awsscout2_rulesets_dir    = os.path.join(awsscout2_rules_data_dir, 'rulesets')
