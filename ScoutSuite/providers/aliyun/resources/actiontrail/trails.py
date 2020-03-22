from ScoutSuite.providers.aliyun.resources.base import AliyunResources


class Trails(AliyunResources):
    async def fetch_all(self):
        for raw_trail in await self.facade.actiontrail.get_trails():
            id, trail = self._parse_trails(raw_trail)
            self[id] = trail

    def _parse_trails(self, raw_trail):
        trail_dict = {}
        trail_dict['id'] = raw_trail.get('Name')
        trail_dict['name'] = raw_trail.get('Name')
        trail_dict['role_name'] = raw_trail.get('RoleName')
        trail_dict['home_region'] = raw_trail.get('HomeRegion')
        trail_dict['oss_bucket_name'] = raw_trail.get('OssBucketName')
        trail_dict['include_global_service_event'] = raw_trail.get('IncludeGlobalServiceEvent')
        trail_dict['status'] = raw_trail.get('Status')
        trail_dict['oss_key_prefix'] = raw_trail.get('OssKeyPrefix')
        trail_dict['region'] = raw_trail.get('Region')
        trail_dict['event_rw'] = raw_trail.get('EventRW')
        trail_dict['type'] = raw_trail.get('Type')
        trail_dict['sls_write_role_arn'] = raw_trail.get('SlsWriteRoleArn')
        trail_dict['sls_project_arn'] = raw_trail.get('SlsProjectArn')
        return trail_dict['id'], trail_dict

