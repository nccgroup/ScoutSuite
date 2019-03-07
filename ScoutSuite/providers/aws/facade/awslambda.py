from ScoutSuite.providers.aws.facade.utils import AWSFacadeUtils


class LambdaFacade:
    async def get_functions(self, region):
        return await AWSFacadeUtils.get_all_pages('lambda', region, 'list_functions', 'Functions')
