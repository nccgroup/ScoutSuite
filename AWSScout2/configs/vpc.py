# -*- coding: utf-8 -*-
"""
Base class for vpc-specific services
"""

class VPCConfig(object):
    """
    Configuration for a single VPC in a single service
    """

    def __init__(self, name = None, resource_types = []):
        self.name = name
        for resource_type in resource_types:
            setattr(self, resource_type, {})
