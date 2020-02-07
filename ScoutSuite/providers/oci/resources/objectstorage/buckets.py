from ScoutSuite.providers.oci.resources.base import OracleResources
from ScoutSuite.providers.oci.facade.base import OracleFacade


class Buckets(OracleResources):
    def __init__(self, facade: OracleFacade):
        super(Buckets, self).__init__(facade)

    async def fetch_all(self):

        namespace = await self.facade.objectstorage.get_namespace()

        for raw_bucket in await self.facade.objectstorage.get_buckets(namespace):
            id, bucket = await self._parse_bucket(raw_bucket)
            self[id] = bucket

    async def _parse_bucket(self, raw_bucket):
        bucket_dict = {}

        bucket_dict['id'] = bucket_dict['name'] = raw_bucket.name
        bucket_dict['compartment_id'] = raw_bucket.compartment_id
        bucket_dict['namespace'] = raw_bucket.namespace
        bucket_dict['created_by'] = raw_bucket.created_by
        bucket_dict['etag'] = raw_bucket.etag
        bucket_dict['freeform_tags'] = list(raw_bucket.freeform_tags) if raw_bucket.freeform_tags else []
        bucket_dict['defined_tags'] = list(raw_bucket.defined_tags) if raw_bucket.defined_tags else []

        raw_bucket_details = await self.facade.objectstorage.get_bucket_details(raw_bucket.namespace,
                                                                                raw_bucket.name)

        bucket_dict['kms_key_id'] = raw_bucket_details.kms_key_id if raw_bucket_details else None
        bucket_dict['approximate_count'] = raw_bucket_details.approximate_count if raw_bucket_details else None
        bucket_dict['time_created'] = raw_bucket_details.time_created if raw_bucket_details else None
        bucket_dict['public_access_type'] = raw_bucket_details.public_access_type if raw_bucket_details else None
        bucket_dict['approximate_size'] = raw_bucket_details.approximate_size if raw_bucket_details else None
        bucket_dict['storage_tier'] = raw_bucket_details.storage_tier if raw_bucket_details else None
        bucket_dict['metadata'] = list(raw_bucket_details.metadata) if raw_bucket_details else None
        bucket_dict['object_lifecycle_policy_etag'] = raw_bucket_details.object_lifecycle_policy_etag if \
            raw_bucket_details else None

        # objects = await self.facade.objectstorage.get_bucket_objects(bucket_dict['namespace'],
        #                                                              bucket_dict['name'])

        return bucket_dict['id'], bucket_dict

