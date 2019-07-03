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
        bucket_dict['name'] = bucket_dict['id'] = raw_bucket.name
        bucket_dict['compartment_id'] = raw_bucket.compartment_id
        bucket_dict['defined_tags'] = raw_bucket.defined_tags
        bucket_dict['namespace'] = raw_bucket.namespace
        bucket_dict['freeform_tags'] = raw_bucket.freeform_tags
        bucket_dict['created_by'] = raw_bucket.created_by
        bucket_dict['etag'] = raw_bucket.etag
        bucket_dict['time_created'] = raw_bucket.time_created

        objects = await self.facade.objectstorage.get_bucket_objects(bucket_dict['namespace'],
                                                                     bucket_dict['name'])

        return bucket_dict['id'], bucket_dict

