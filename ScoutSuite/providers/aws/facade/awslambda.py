from ScoutSuite.providers.aws.facade.utils import AWSFacadeUtils
from ScoutSuite.providers.aws.facade.basefacade import AWSBaseFacade


class LambdaFacade(AWSBaseFacade):
    async def get_functions(self, region):
        return await AWSFacadeUtils.get_all_pages('lambda', region, self.session, 'list_functions', 'Functions')
