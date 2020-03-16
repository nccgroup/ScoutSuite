from ScoutSuite.core.console import print_exception
from ScoutSuite.providers.aws.facade.utils import AWSFacadeUtils
from ScoutSuite.providers.aws.facade.basefacade import AWSBaseFacade
from ScoutSuite.providers.utils import run_concurrently


class ConfigFacade(AWSBaseFacade):

    async def get_rules(self, region):
        try:
            return await AWSFacadeUtils.get_all_pages('config', region, self.session, 'describe_config_rules', 'ConfigRules')
        except Exception as e:
            print_exception('Failed to get Config ruless: {}'.format(e))
            return []

    async def get_recorders(self, region: str):
        client = AWSFacadeUtils.get_client('config', self.session, region)

        try:
            recorders = (await run_concurrently(client.describe_configuration_recorders))['ConfigurationRecorders']
        except Exception as e:
            print_exception('Failed to get Config recorders: {}'.format(e))
            recorders = []

        try:
            recorder_statuses_list = \
                (await run_concurrently(client.describe_configuration_recorder_status))['ConfigurationRecordersStatus']
        except Exception as e:
            print_exception('Failed to get Config recorder statuses: {}'.format(e))
        else:
            # To accelerate the mapping of the statuses, we preprocess the data by creating a
            # <recorder_name: recorder_status> map. This prevents having to iterate over the list of statuses for each
            # recorder.
            recorder_statuses_map = {recorder['name']: recorder for recorder in recorder_statuses_list}
            for recorder in recorders:
                recorder['ConfigurationRecordersStatus'] = recorder_statuses_map[recorder['name']]

        return recorders
