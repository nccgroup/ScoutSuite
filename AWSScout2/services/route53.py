# -*- coding: utf-8 -*-

from opinel.utils.aws import handle_truncated_response
from opinel.utils.console import printError, printException
from opinel.utils.globals import manage_dictionary

from AWSScout2.configs.base import BaseConfig



class Route53DomainsConfig(BaseConfig):
    """
    Object that holds the Route53Domains configuration
    """

    targets = (
        ('domains', 'Domains', 'list_domains', {}, False),
    )

    def __init__(self, target_config):
        self.domains = {}
        self.domains_count = 0
        super(Route53DomainsConfig, self).__init__(target_config)



    ########################################
    ##### Domains
    ########################################
    def parse_domains(self, domain, params):
        """
        Parse a single Route53Domains domain
        """
        domain_id = self.get_non_aws_id(domain['DomainName'])
        domain['name'] = domain.pop('DomainName')
        #TODO: Get Dnssec info when available
        #api_client = params['api_client']
        #details = api_client.get_domain_detail(DomainName = domain['name'])
        #get_keys(details, domain, ['Dnssec'])
        self.domains[domain_id] = domain



class Route53Config(BaseConfig):
    """
    Object that holds the Route53 configuration
    """

    targets = (
        ('hosted_zones', 'HostedZones', 'list_hosted_zones', {}, False),
    )

    def __init__(self, target_config):
        self.hosted_zones = {}
        self.hosted_zones_count = 0
        super(Route53Config, self).__init__(target_config)



    ########################################
    ##### hosted_zoness
    ########################################
    def parse_hosted_zones(self, hosted_zone, params):
        """
        Parse a single Route53hosted_zoness hosted_zones
        """
        # When resuming upon throttling error, skip if already fetched
        hosted_zone_id = hosted_zone.pop('Id')
        hosted_zone['name'] = hosted_zone.pop('Name')
        api_client = params['api_client']
        record_sets = handle_truncated_response(api_client.list_resource_record_sets, {'HostedZoneId': hosted_zone_id}, ['ResourceRecordSets'])
        hosted_zone.update(record_sets)
        #print(str(record_sets))
        #record_sets = api_client.list_resource_record_sets()
        #hosted_zone['RecordSets'] = record_sets['Resourc']
        self.hosted_zones[hosted_zone_id] = hosted_zone
