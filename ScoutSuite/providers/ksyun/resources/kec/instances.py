from ScoutSuite.providers.ksyun.resources.base import KsyunResources
from ScoutSuite.providers.ksyun.facade.base import KsyunFacade


class Instances(KsyunResources):
    def __init__(self, facade: KsyunFacade, region: str):
        super().__init__(facade)
        self.region = region

    async def fetch_all(self):
        for raw_instance in await self.facade.kec.get_instances(region=self.region):
            id, instance = await self._parse_instance(raw_instance)
            self[id] = instance

    async def _parse_instance(self, raw_instance):
        instance_dict = {}
        instance_dict['id'] = raw_instance.get('InstanceId')
        instance_dict['name'] = raw_instance.get('InstanceName')
        instance_dict['creation_time'] = raw_instance.get('CreationDate')
        instance_dict['os_type'] = raw_instance.get('Platform')
        instance_dict['host_name'] = raw_instance.get('HostName')
        instance_dict['image_id'] = raw_instance.get('ImageId')
        instance_dict['instance_type'] = raw_instance.get('InstanceType')
        instance_dict['eip_address'] = raw_instance.get('EipAddress')
        instance_dict['deletion_protection'] = raw_instance.get('DeletionProection')

        return instance_dict['id'], instance_dict