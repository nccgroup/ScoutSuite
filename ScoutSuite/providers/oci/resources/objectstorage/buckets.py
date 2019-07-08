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

        raw_bucket_details = await self.facade.objectstorage.get_bucket_details(raw_bucket.namespace,
                                                                                raw_bucket.name)

        bucket_dict['id'] = bucket_dict['name'] = raw_bucket_details.name
        bucket_dict['kms_key_id'] = raw_bucket_details.kms_key_id
        bucket_dict['compartment_id'] = raw_bucket_details.compartment_id
        bucket_dict['approximate_count'] = raw_bucket_details.approximate_count
        bucket_dict['namespace'] = raw_bucket_details.namespace
        bucket_dict['created_by'] = raw_bucket_details.created_by
        bucket_dict['etag'] = raw_bucket_details.etag
        bucket_dict['time_created'] = raw_bucket_details.time_created
        bucket_dict['public_access_type'] = raw_bucket_details.public_access_type
        bucket_dict['approximate_size'] = raw_bucket_details.approximate_size
        bucket_dict['storage_tier'] = raw_bucket_details.storage_tier
        bucket_dict['metadata'] = list(raw_bucket_details.metadata)
        bucket_dict['freeform_tags'] = list(raw_bucket_details.freeform_tags)
        bucket_dict['defined_tags'] = list(raw_bucket_details.defined_tags)
        bucket_dict['object_lifecycle_policy_etag'] = raw_bucket_details.object_lifecycle_policy_etag

        # objects = await self.facade.objectstorage.get_bucket_objects(bucket_dict['namespace'],
        #                                                              bucket_dict['name'])

        return bucket_dict['id'], bucket_dict

