from ScoutSuite.providers.ksyun.resources.base import KsyunResources


class Buckets(KsyunResources):
    async def fetch_all(self):
        for raw_bucket in await self.facade.ks3.get_buckets():
            id, bucket = self._parse_bucket(raw_bucket)
            self[id] = bucket

    def _parse_bucket(self, raw_bucket):
        bucket_dict = {}
        bucket_dict['name'] = bucket_dict['id'] = raw_bucket.name
        bucket_dict['location'] = raw_bucket.location
        bucket_dict['storage_class'] = raw_bucket.storage_class
        bucket_dict['creation_date'] = raw_bucket.creation_date
        return bucket_dict['id'], bucket_dict
