#!/usr/bin/env python

from AWSScout2.finding import *

import datetime
import dateutil.parser
import re

class Ec2Finding(Finding):

    def __init__(self, description, name, entity, callback, callback_args, idprefix, level):
        self.keyword_prefix = 'ec2'
        Finding.__init__(self, description, name, entity, callback, callback_args, idprefix, level)
