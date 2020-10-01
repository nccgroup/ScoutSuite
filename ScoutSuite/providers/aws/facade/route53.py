from ScoutSuite.core.console import print_exception
from ScoutSuite.providers.aws.facade.basefacade import AWSBaseFacade
from ScoutSuite.providers.aws.facade.utils import AWSFacadeUtils


class Route53Facade(AWSBaseFacade):
    async def get_domains(self, region):
        try:
            return await AWSFacadeUtils.get_all_pages('route53domains', region, self.session,
                                                      'list_domains', 'Domains')
        except Exception as e:
            print_exception(f'Failed to get Route53 domains: {e}')
            return []

    async def get_hosted_zones(self):
        try:
            return await AWSFacadeUtils.get_all_pages('route53', None, self.session,
                                                      'list_hosted_zones', 'HostedZones')
        except Exception as e:
            print_exception(f'Failed to get Route53 hosted zones: {e}')

    async def get_resource_records(self, hosted_zone_id):
        try:
            return await AWSFacadeUtils.get_all_pages('route53', None, self.session,
                                                      'list_resource_record_sets', 'ResourceRecordSets',
                                                      HostedZoneId=hosted_zone_id)
        except Exception as e:
            print_exception(f'Failed to get Route53 resource records: {e}')
