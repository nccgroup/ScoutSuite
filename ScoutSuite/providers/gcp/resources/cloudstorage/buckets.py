from ScoutSuite.providers.base.resources.base import Resources
from ScoutSuite.providers.gcp.facade.base import GCPFacade
from ScoutSuite.providers.utils import get_non_provider_id


class Buckets(Resources):
    def __init__(self, facade: GCPFacade, project_id: str):
        super(Buckets, self).__init__(facade)
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
            bucket_dict['acls'] = list(raw_bucket.acl)
            bucket_dict['default_object_acl'] = list(raw_bucket.default_object_acl)
        
        bucket_dict['acl_configuration'] = self._get_cloudstorage_bucket_acl(raw_bucket)  # FIXME this should be "IAM"
        return bucket_dict['id'], bucket_dict

    def _get_cloudstorage_bucket_acl(self, raw_bucket):
        bucket_acls = raw_bucket.iam_policy
        acl_config = {}
        if bucket_acls:
            for role in bucket_acls._bindings:
                if 'legacy' not in role:
                    for member in bucket_acls[role]:
                        if member not in acl_config:
                            acl_config[member] = [role]
                        else:
                            acl_config[member].append(role)
        return acl_config
