import asyncio

from ScoutSuite.providers.aws.resources.resources import AWSCompositeResources
from ScoutSuite.providers.aws.resources.iam.credentialreports import CredentialReports
from ScoutSuite.providers.aws.resources.iam.groups import Groups
from ScoutSuite.providers.aws.resources.iam.policies import Policies
from ScoutSuite.providers.aws.facade.facade import AWSFacade


class IAM(AWSCompositeResources):
    _children = [
        (CredentialReports, 'credential_reports'),
        (Groups, 'groups'),
        (Policies, 'policies')
    ]

    def __init__(self):
        # TODO: Should be injected
        self.facade = AWSFacade()
        self.service = 'iam'

    async def fetch_all(self, credentials, regions=None, partition_name='aws'):
        # TODO: This should not be set here, the facade should be injected and already authenticated
        self.facade._set_session(credentials)
        await self._fetch_children(self, {})
