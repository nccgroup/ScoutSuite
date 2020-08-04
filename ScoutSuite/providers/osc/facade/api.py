from osc_sdk_python import Gateway

from ScoutSuite.core.console import print_exception
from ScoutSuite.providers.osc.facade.basefacade import OSCBaseFacade
from ScoutSuite.providers.osc.facade.utils import OSCFacadeUtils


class APIFacade(OSCBaseFacade):
    def __init__(self, session: Gateway):
        self.session = session
        super(APIFacade, self).__init__(session)

    async def get_security_groups(self, region: str, vpc: str = None):
        try:
            security_groups = await OSCFacadeUtils.get_all_security_groups(self.session)
            return security_groups
        except Exception as e:
            print_exception('Failed to describe API security groups: {}'.format(e))
            return []

    async def get_volumes(self):
        try:
            volumes = await OSCFacadeUtils.get_all_volumes(self.session)
            return volumes
        except Exception as e:
            print_exception('Failed to describe API volumes: {}'.format(e))
            return []

    async def get_snapshots(self, region: str):
        try:
            snapshots = await OSCFacadeUtils.get_all_snapshots(self.session)
            return snapshots
        except Exception as e:
            print_exception('Failed to describe API snapshots: {}'.format(e))
            return []
