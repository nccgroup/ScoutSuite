from ScoutSuite.providers.aws.resources.regions import Regions
from ScoutSuite.providers.aws.resources.resources import AWSResources


class RDSInstances(AWSResources):
    async def fetch_all(self, **kwargs):
        raw_instances = await self.facade.rds.get_instances(self.scope['region'], self.scope['vpc'])
        for raw_instance in raw_instances:
            name, resource = self._parse_instance(raw_instance)
            self[name] = resource

    def _parse_instance(self, raw_instance):
        instance = {}
        instance['name'] = raw_instance.pop('DBInstanceIdentifier')
        for key in ['InstanceCreateTime', 'Engine', 'DBInstanceStatus', 'AutoMinorVersionUpgrade',
                    'DBInstanceClass', 'MultiAZ', 'Endpoint', 'BackupRetentionPeriod', 'PubliclyAccessible',
                    'StorageEncrypted', 'VpcSecurityGroups', 'DBSecurityGroups', 'DBParameterGroups',
                    'EnhancedMonitoringResourceArn', 'StorageEncrypted']:
            instance[key] = raw_instance[key] if key in raw_instance else None

        return instance['name'], instance
