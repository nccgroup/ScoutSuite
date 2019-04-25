from ScoutSuite.core.console import print_exception
from ScoutSuite.providers.aws.facade.utils import AWSFacadeUtils
from ScoutSuite.providers.aws.facade.basefacade import AWSBaseFacade
from ScoutSuite.providers.utils import run_concurrently


class ConfigFacade(AWSBaseFacade):
    async def get_rules(self, region):
        return await AWSFacadeUtils.get_all_pages('config', region, self.session, 'describe_config_rules', 'ConfigRules')

    async def get_recorder_status(self, region):
        client = AWSFacadeUtils.get_client('config', self.session, region)
        try:
            recorder_status = await run_concurrently(
                lambda: client.describe_configuration_recorder_status())
        except Exception as e:
            print_exception('Failed to describe recorder status: {}'.format(e))
        else:
            return recorder_status['ConfigurationRecordersStatus']
