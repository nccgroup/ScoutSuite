from ScoutSuite.providers.aws.facade.base import AWSFacade
from ScoutSuite.providers.aws.resources.base import AWSCompositeResources
from ScoutSuite.providers.utils import get_non_provider_id

from .identity_policies import IdentityPolicies


class Identities(AWSCompositeResources):
    _children = [
        (IdentityPolicies, 'policies')
    ]

    def __init__(self, facade: AWSFacade, region: str):
        super(Identities, self).__init__(facade)
        self.region = region

    async def fetch_all(self):
        raw_identities = await self.facade.ses.get_identities(self.region)
        for raw_identity in raw_identities:
            id, identity = self._parse_identity(raw_identity)
            self[id] = identity

        await self._fetch_children_of_all_resources(
            resources=self,
            scopes={identity_id: {'region': self.region, 'identity_name': identity['name']}
                    for (identity_id, identity) in self.items()}
        )

    def _parse_identity(self, raw_identity):
        identity_name, dkim_attributes = raw_identity
        identity = {}
        identity['name'] = identity_name
        identity['DkimEnabled'] = dkim_attributes['DkimEnabled']
        identity['DkimVerificationStatus'] = dkim_attributes['DkimVerificationStatus']

        return get_non_provider_id(identity_name), identity
