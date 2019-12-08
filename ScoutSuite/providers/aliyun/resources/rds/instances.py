from ScoutSuite.providers.aliyun.resources.base import AliyunResources
from ScoutSuite.providers.aliyun.facade.base import AliyunFacade


class Instances(AliyunResources):
    def __init__(self, facade: AliyunFacade, region: str):
        super(Instances, self).__init__(facade)
        self.region = region

    async def fetch_all(self):
        for raw_instance in await self.facade.rds.get_instances(region=self.region):
            id, instance = await self._parse_instance(raw_instance)
            self[id] = instance

    async def _parse_instance(self, raw_instance):
        instance_dict = {}

        instance_dict['id'] = raw_instance.get('DBInstanceId')
        instance_dict['name'] = raw_instance.get('DBInstanceDescription', raw_instance.get('DBInstanceId'))
        instance_dict['create_time'] = raw_instance.get('CreateTime')
        instance_dict['expire_time'] = raw_instance.get('ExpireTime')
        instance_dict['ins_id'] = raw_instance.get('InsId')
        instance_dict['lock_mode'] = raw_instance.get('LockMode')
        instance_dict['db_instance_net_type'] = raw_instance.get('DBInstanceNetType')
        instance_dict['read_only_db_instance_ids'] = raw_instance.get('ReadOnlyDBInstanceIds')
        instance_dict['lock_reason'] = raw_instance.get('LockReason')
        instance_dict['engine'] = raw_instance.get('Engine')
        instance_dict['vpc_id'] = raw_instance.get('VpcId')
        instance_dict['mutri_o_rsignle'] = raw_instance.get('MutriORsignle')
        instance_dict['connection_mode'] = raw_instance.get('ConnectionMode')
        instance_dict['region_id'] = raw_instance.get('RegionId')
        instance_dict['resource_group_id'] = raw_instance.get('ResourceGroupId')
        instance_dict['vswitch_id'] = raw_instance.get('VSwitchId')
        instance_dict['instance_network_type'] = raw_instance.get('InstanceNetworkType')
        instance_dict['db_instance_type'] = raw_instance.get('DBInstanceType')
        instance_dict['db_instance_status'] = raw_instance.get('DBInstanceStatus')
        instance_dict['zone_id'] = raw_instance.get('ZoneId')
        instance_dict['engine_version'] = raw_instance.get('EngineVersion')
        instance_dict['vpc_cloud_instance_id'] = raw_instance.get('VpcCloudInstanceId')
        instance_dict['pay_type'] = raw_instance.get('PayType')
        instance_dict['db_instance_class'] = raw_instance.get('DBInstanceClass')

        return instance_dict['id'], instance_dict

