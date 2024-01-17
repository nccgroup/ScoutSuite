from google.cloud import storage
from google.cloud import orgpolicy_v2
from google.api_core.gapic_v1.client_info import ClientInfo

from ScoutSuite.providers.gcp.facade.utils import GCPFacadeUtils

from ScoutSuite.core.console import print_exception
from ScoutSuite.providers.utils import run_concurrently, get_and_set_concurrently
from ScoutSuite.utils import get_user_agent


class CloudStorageFacade:

    def get_client(self, project_id: str):
        client_info = ClientInfo(user_agent=get_user_agent())
        client = storage.Client(project=project_id,
                                client_info=client_info)
        return client

    def get_org_policy_client(self):
        client_info = ClientInfo(user_agent=get_user_agent())
        client = orgpolicy_v2.OrgPolicyClient(client_info=client_info)
        return client

    async def get_buckets(self, project_id: str):
        try:
            client = self.get_client(project_id)
            buckets = await run_concurrently(lambda: list(client.list_buckets()))
            await get_and_set_concurrently([self._get_and_set_bucket_logging,
                                            self._get_and_set_bucket_iam_policy,
                                            self._get_and_set_public_access_prevention],
                                           buckets, project_id=project_id)
            return buckets
        except Exception as e:
            print_exception(f'Failed to retrieve storage buckets: {e}')
            return []

    async def _get_and_set_bucket_logging(self, bucket, **kwargs):
        try:
            bucket_logging = await run_concurrently(lambda: bucket.get_logging())
            setattr(bucket, 'logging', bucket_logging)
        except Exception as e:
            print_exception(f'Failed to retrieve bucket logging: {e}')
            setattr(bucket, 'logging', None)

    async def _get_and_set_bucket_iam_policy(self, bucket, **kwargs):
        try:
            bucket_iam_policy = await run_concurrently(lambda: bucket.get_iam_policy())
            setattr(bucket, 'iam_policy', bucket_iam_policy)
        except Exception as e:
            print_exception(f'Failed to retrieve bucket IAM policy: {e}')
            setattr(bucket, 'iam_policy',  None)

    async def _get_and_set_public_access_prevention(self, bucket, project_id):
        try:
            org_client = self.get_org_policy_client()
            request = orgpolicy_v2.GetEffectivePolicyRequest(name=f"projects/{project_id}/policies/storage.publicAccessPrevention")
            response = org_client.get_effective_policy(request=request)
            setattr(bucket, 'effective_public_access_prevention',
                    'enforce: true' in str(response.spec.rules)
                    )
        except Exception as e:
            print_exception(f'Failed to retrieve organization policy storage.publicAccessPrevention: {e}')
            setattr(bucket, 'effective_public_access_prevention', None)
