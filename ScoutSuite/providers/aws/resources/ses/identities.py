from ScoutSuite.providers.aws.resources.resources import AWSCompositeResources
from ScoutSuite.providers.utils import get_non_provider_id

from .identity_policies import IdentityPolicies


class Identities(AWSCompositeResources):
    _children = [
        (IdentityPolicies, 'policies')
    ]

    async def fetch_all(self, **kwargs):
        raw_identities = await self.facade.ses.get_identities(self.scope['region'])
        # TODO: parallelize the following async loop:
        for raw_identity in raw_identities:
            id, identity = self._parse_identity(raw_identity)
            await self._fetch_children(
                parent=identity,
                scope={'region': self.scope['region'], 'identity_name': identity['name']}
            )
            self[id] = identity

    def _parse_identity(self, raw_identity):
        identity_name, dkim_attributes = raw_identity
        identity = {}
        identity['name'] = identity_name
        identity['DkimEnabled'] = dkim_attributes['DkimEnabled']
        identity['DkimVerificationStatus'] = dkim_attributes['DkimVerificationStatus']

        return get_non_provider_id(identity_name), identity
