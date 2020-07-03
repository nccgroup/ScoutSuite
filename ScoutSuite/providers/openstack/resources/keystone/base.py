from ScoutSuite.providers.openstack.facade.base import OpenstackFacade
from ScoutSuite.providers.openstack.resources.base import OpenstackCompositeResources
from ScoutSuite.providers.openstack.resources.keystone.domains import Domains
from ScoutSuite.providers.openstack.resources.keystone.groups import Groups
from ScoutSuite.providers.openstack.resources.keystone.policies import Policies
from ScoutSuite.providers.openstack.resources.keystone.projects import Projects
from ScoutSuite.providers.openstack.resources.keystone.regions import Regions
from ScoutSuite.providers.openstack.resources.keystone.tokens import Tokens
from ScoutSuite.providers.openstack.resources.keystone.users import Users


class Keystone(OpenstackCompositeResources):
    _children = [
        (Domains, 'domains'),
        (Groups, 'groups'),
        (Policies, 'policies'),
        (Projects, 'projects'),
        (Regions, 'regions'),
        (Tokens, 'tokens'),
        (Users, 'users'),
    ]

    def __init__(self, facade: OpenstackFacade):
        super(Keystone, self).__init__(facade)
        self.service = 'keystone'

    async def fetch_all(self, **kwargs):
        await self._fetch_children(resource_parent=self)

    async def finalize(self):
        return
