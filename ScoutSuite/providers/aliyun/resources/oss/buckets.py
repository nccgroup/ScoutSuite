from ScoutSuite.providers.aliyun.resources.base import AliyunResources
from ScoutSuite.core.console import print_exception


class Buckets(AliyunResources):
    async def fetch_all(self):
        parsing_error_counter = 0
        for raw_bucket in await self.facade.oss.get_buckets():
            try:
                id, bucket = self._parse_bucket(raw_bucket)
                self[id] = bucket
            except Exception as e:
                parsing_error_counter += 1
        if parsing_error_counter > 0:
            print_exception(
                'Failed to parse {} resource: {} times'.format(self.__class__.__name__, parsing_error_counter))

    def _parse_bucket(self, raw_bucket):
        bucket_dict = {}
        bucket_dict['name'] = bucket_dict['id'] = raw_bucket.name
        bucket_dict['location'] = raw_bucket.location
        bucket_dict['storage_class'] = raw_bucket.storage_class
        bucket_dict['creation_date'] = raw_bucket.creation_date
        return bucket_dict['id'], bucket_dict
