
from ScoutSuite.providers.ksyun.facade.base import KsyunFacade
from ScoutSuite.providers.ksyun.resources.base import KsyunResources


class Buckets(KsyunResources):
    # def __init__(self, facade: KsyunFacade, region: str):
    #     super().__init__(facade)
    #     self.region = region

    async def fetch_all(self):
        for raw_bucket in await self.facade.ks3.get_buckets():
            id, bucket = self._parse_bucket(raw_bucket)
            self[id] = bucket

    def _parse_bucket(self, raw_bucket):
        bucket_dict = {}
        bucket_dict['name'] = bucket_dict['id'] = raw_bucket.get('name')
        bucket_dict['location'] = raw_bucket.get('region')
        bucket_dict['storage_class'] = raw_bucket.get('type')
        bucket_dict['creation_date'] = raw_bucket.get('creationDate')
        return bucket_dict['id'], bucket_dict
