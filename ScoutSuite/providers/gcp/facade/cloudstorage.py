from google.cloud import storage
from google.cloud import orgpolicy_v2
from google.api_core.gapic_v1.client_info import ClientInfo

from ScoutSuite.providers.gcp.facade.basefacade import GCPBaseFacade

from ScoutSuite.core.console import print_exception, print_warning
from ScoutSuite.providers.utils import run_concurrently, get_and_set_concurrently
from ScoutSuite.utils import get_user_agent


class CloudStorageFacade(GCPBaseFacade):

    def __init__(self):
        super().__init__('cloudresourcemanager', 'v1')

    def _get_effective_public_access_prevention(self, project_id):
        try:
            resourcemanager_client = self._get_client()
            request = resourcemanager_client.projects().getEffectiveOrgPolicy(resource=f"projects/{project_id}",
                                                                              body={
                                                                                  "constraint": f"constraints/storage.publicAccessPrevention"})
            response = request.execute()
            return response.get('booleanPolicy', {}).get('enforced', False)
        except Exception as e:
            print_warning(f'Failed to retrieve project {project_id} storage.publicAccessPrevention constraint: {e}')
            return None

    def get_storage_client(self, project_id: str):
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
            client = self.get_storage_client(project_id)
            buckets = await run_concurrently(lambda: list(client.list_buckets()))
            await get_and_set_concurrently([self._get_and_set_bucket_logging,
                                            self._get_and_set_bucket_iam_policy,
                                            self._get_and_set_public_access_prevention],
                                           buckets,
                                           effective_public_access_prevention=self._get_effective_public_access_prevention(
                                               project_id))
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
            setattr(bucket, 'iam_policy', None)

    async def _get_and_set_public_access_prevention(self, bucket, effective_public_access_prevention):
        try:
            setattr(bucket, 'effective_public_access_prevention', effective_public_access_prevention)
        except Exception as e:
            print_exception(f'Failed to set effective public access prevention for bucket {bucket}: {e}')
            setattr(bucket, 'effective_public_access_prevention', None)
