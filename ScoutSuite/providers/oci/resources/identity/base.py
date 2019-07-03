from ScoutSuite.providers.oci.resources.base import OracleCompositeResources
from ScoutSuite.providers.oci.resources.identity.users import Users
from ScoutSuite.providers.oci.resources.identity.groups import Groups
from ScoutSuite.providers.oci.resources.identity.policies import Policies
from ScoutSuite.providers.oci.facade.base import OracleFacade


class Identity(OracleCompositeResources):
    _children = [
        (Users, 'users'),
        (Groups, 'groups'),
        (Policies, 'policies'),
    ]

    def __init__(self, facade: OracleFacade):
        super(Identity, self).__init__(facade)
        self.service = 'identity'

    async def fetch_all(self, **kwargs):
        await self._fetch_children(resource_parent=self)

