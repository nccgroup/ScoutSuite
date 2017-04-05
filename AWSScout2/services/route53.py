# -*- coding: utf-8 -*-

from opinel.utils import connect_service, handle_truncated_response, manage_dictionary, printError, printException

from AWSScout2.configs.base import BaseConfig



class Route53DomainsConfig(BaseConfig):
    """
    Object that holds the Route53Domains configuration

    :ivar credential_report:    Credential report as downloaded from the AWS API
    :ivar groups:               Dictionary of Route53Domains groups in the AWS account
    :ivar groups_count:         len(groups)
    :ivar password_policy:      Account password policy
    :ivar permissions:          Summary of permissions granted via all Route53Domains policies
    :ivar policies:             Dictionary of Route53Domains managed policies in use within the AWS Account
    :ivar policies_count:       len(policies)
    :ivar roles:                Dictionary of Route53Domains roles in the AWS account
    :ivar roles_count:          len(roles)
    :ivar users:                Dictionary of Route53Domains users in the AWS account
    :ivar users_count:          len(users)
    """

    targets = (
        ('domains', 'Domains', 'list_domains', {}, False),
    )

    def __init__(self):
        self.domains = {}
        self.domains_count = 0
        super(Route53DomainsConfig, self).__init__()



    ########################################
    ##### Domains
    ########################################
    def parse_domains(self, domain, params):
        """
        Parse a single Route53Domains domain
        """
        # When resuming upon throttling error, skip if already fetched
        domain_id = self.get_non_aws_id(domain['DomainName'])
        domain['name'] = domain.pop('DomainName')
        # TODO: Get Dnssec info when available
        #api_client = params['api_client']
        #details = api_client.get_domain_detail(DomainName = domain['name'])
        #get_keys(details, domain, ['Dnssec'])
        self.domains[domain_id] = domain
