from ScoutSuite.providers.aws.facade.utils import AWSFacadeUtils
from ScoutSuite.providers.aws.facade.basefacade import AWSBaseFacade


class Route53Facade(AWSBaseFacade):
    async def get_domains(self, region):
        return await AWSFacadeUtils.get_all_pages('route53domains', region, self.session, 'list_domains', 'Domains')
