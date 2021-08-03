from ScoutSuite.providers.aws.resources.organizations.accounts import Accounts
from ScoutSuite.providers.aws.facade.base import AWSFacade
from ScoutSuite.providers.aws.resources.organizations.accounts import Accounts
from ScoutSuite.providers.aws.resources.organizations.organizational_units import OrganizationalUnits
from ScoutSuite.providers.aws.resources.organizations.service_policies import ServicePolicies
from ScoutSuite.providers.aws.resources.organizations.tag_policies import TagPolicies
from ScoutSuite.providers.aws.resources.organizations.backup_policies import BackupPolicies
from ScoutSuite.providers.aws.resources.organizations.optout_policies import OptOutPolicies
from ScoutSuite.providers.aws.resources.base import AWSCompositeResources


class Organizations(AWSCompositeResources):
    _children = [
        (Accounts, "accounts"),
        (OrganizationalUnits, "organizational_units"),
        (ServicePolicies, "service_policies"),
        (TagPolicies, "tag_policies"),
        (BackupPolicies, "backup_policies"),
        (OptOutPolicies, "optout_policies"),
    ]

    def __init__(self, facade: AWSFacade):
        super().__init__(facade)
        self.service = "organizations"

    async def fetch_all(self, partition_name="aws", **kwargs):
        await self._fetch_children(self)
