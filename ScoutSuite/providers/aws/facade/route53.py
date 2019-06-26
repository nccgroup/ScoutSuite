from ScoutSuite.core.console import print_exception
from ScoutSuite.providers.aws.facade.basefacade import AWSBaseFacade
from ScoutSuite.providers.aws.facade.utils import AWSFacadeUtils


class Route53Facade(AWSBaseFacade):
    async def get_domains(self, region):
        try:
            return await AWSFacadeUtils.get_all_pages('route53domains', region, self.session, 'list_domains', 'Domains')
        except Exception as e:
            print_exception('Failed to get Route53 domains: {}'.format(e))
            return []
