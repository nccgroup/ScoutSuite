from ScoutSuite.core.console import print_error
from ScoutSuite.providers.base.configs.resources import Resources
from ScoutSuite.providers.gcp.facade.gcp import GCPFacade
from ScoutSuite.providers.utils import get_non_provider_id

class Buckets(Resources):
    def __init__(self, gcp_facade: GCPFacade, project_id: str):
        self.gcp_facade = gcp_facade
        self.project_id = project_id

    async def fetch_all(self):
        raw_buckets = await self.gcp_facade.cloudstorage.get_buckets(self.project_id)
        for raw_bucket in raw_buckets:
            bucket_id, bucket = self._parse_bucket(raw_bucket)
            self[bucket_id] = bucket

    def _parse_bucket(self, raw_bucket):
        bucket_dict = {}
        bucket_dict['id'] = get_non_provider_id(raw_bucket.id)
        bucket_dict['name'] = raw_bucket.name

        for project in self.projects:
            if str(project['projectNumber']) == str(raw_bucket.project_number):
                bucket_dict['project_id'] = project['projectId']
                break

        bucket_dict['project_number'] = raw_bucket.project_number
        bucket_dict['creation_date'] = raw_bucket.time_created
        bucket_dict['location'] = raw_bucket.location
        bucket_dict['storage_class'] = raw_bucket.storage_class.lower()
        bucket_dict['versioning_status_enabled'] = raw_bucket.versioning_enabled
        bucket_dict['logging_enabled'] = self._is_logging_enabled(raw_bucket)

        get_cloudstorage_bucket_acl(raw_bucket, bucket_dict)

        return bucket_dict['id'], bucket_dict

    def _is_logging_enabled(raw_bucket):
        try:
            return raw_bucket.get_logging() is not None
        except Exception as e:
            print_error('Failed to get bucket logging configuration for %s: %s' % (raw_bucket.name, e))
            return None # Return False instead?

def get_cloudstorage_bucket_acl(bucket, bucket_dict):
    try:
        bucket_acls = bucket.get_iam_policy()
        bucket_dict['acl_configuration'] = {}
        for role in bucket_acls._bindings:
            for member in bucket_acls[role]:
                if member.split(':')[0] not in ['projectEditor', 'projectViewer', 'projectOwner']:
                    if member not in bucket_dict['acl_configuration']:
                        bucket_dict['acl_configuration'][member] = [role]
                    else:
                        bucket_dict['acl_configuration'][member].append(role)
        return True
    except Exception as e:
        print_error('Failed to get bucket ACL configuration for %s: %s' % (bucket.name, e))
        bucket_dict['acls'] = 'Unknown'
        return False