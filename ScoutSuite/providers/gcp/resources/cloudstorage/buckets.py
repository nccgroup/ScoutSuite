from ScoutSuite.providers.base.resources.base import Resources
from ScoutSuite.providers.gcp.facade.base import GCPFacade
from ScoutSuite.providers.utils import get_non_provider_id
from ScoutSuite.core.console import print_exception


class Buckets(Resources):
    def __init__(self, facade: GCPFacade, project_id: str):
        super().__init__(facade)
        self.project_id = project_id

    async def fetch_all(self):
        raw_buckets = await self.facade.cloudstorage.get_buckets(self.project_id)
        for raw_bucket in raw_buckets:
            bucket_id, bucket = self._parse_bucket(raw_bucket)
            self[bucket_id] = bucket

    def _parse_bucket(self, raw_bucket):
        bucket_dict = {}
        bucket_dict['id'] = get_non_provider_id(raw_bucket.id)
        bucket_dict['name'] = raw_bucket.name
        bucket_dict['project_id'] = self.project_id
        bucket_dict['project_number'] = raw_bucket.project_number
        bucket_dict['creation_date'] = raw_bucket.time_created
        bucket_dict['location'] = raw_bucket.location
        bucket_dict['storage_class'] = raw_bucket.storage_class.lower()
        bucket_dict['versioning_enabled'] = raw_bucket.versioning_enabled
        bucket_dict['logging_enabled'] = raw_bucket.logging is not None

        bucket_dict['public_access_prevention'] = raw_bucket.iam_configuration.public_access_prevention

        iam_configuration = raw_bucket.iam_configuration.get('uniformBucketLevelAccess') or \
            raw_bucket.iam_configuration.get('bucketPolicyOnly')
        if iam_configuration:
            bucket_dict['uniform_bucket_level_access'] = iam_configuration.get("enabled", False)
        else:
            bucket_dict['uniform_bucket_level_access'] = None

        if bucket_dict['uniform_bucket_level_access']:
            bucket_dict['acls'] = []
            bucket_dict['default_object_acl'] = []
        else:
            try:
                bucket_dict['acls'] = list(raw_bucket.acl)
            except Exception as e:
                print_exception(f'Failed to retrieve storage bucket ACLs: {e}')
                bucket_dict['acls'] = []
            try:
                bucket_dict['default_object_acl'] = list(raw_bucket.default_object_acl)
            except Exception as e:
                print_exception(f'Failed to retrieve storage bucket object ACLs: {e}')
                bucket_dict['default_object_acl'] = []

        bucket_dict['member_bindings'] = self._get_cloudstorage_bucket_iam_member_bindings(raw_bucket)

        return bucket_dict['id'], bucket_dict

    def _get_cloudstorage_bucket_iam_member_bindings(self, raw_bucket):
        bucket_iam_policy = raw_bucket.iam_policy
        member_bindings = {}
        if bucket_iam_policy:
            for binding in bucket_iam_policy._bindings:
                for member in binding['members']:
                    if member not in member_bindings:
                        member_bindings[member] = [binding['role']]
                    else:
                        member_bindings[member].append(binding['role'])
        return member_bindings
