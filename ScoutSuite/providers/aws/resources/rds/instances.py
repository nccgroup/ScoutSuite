from ScoutSuite.providers.aws.facade.base import AWSFacade
from ScoutSuite.providers.aws.resources.base import AWSResources
from ScoutSuite.core.console import print_exception


class RDSInstances(AWSResources):
    def __init__(self, facade: AWSFacade, region: str, vpc: str):
        super().__init__(facade)
        self.region = region
        self.vpc = vpc

    async def fetch_all(self):
        raw_instances = await self.facade.rds.get_instances(self.region, self.vpc)
        parsing_error_counter = 0
        for raw_instance in raw_instances:
            try:
                name, resource = self._parse_instance(raw_instance)
                self[name] = resource
            except Exception as e:
                parsing_error_counter += 1
        if parsing_error_counter > 0:
            print_exception(
                'Failed to parse {} resource: {} times'.format(self.__class__.__name__, parsing_error_counter))

    def _parse_instance(self, raw_instance):
        instance = {}
        instance['name'] = raw_instance.pop('DBInstanceIdentifier')
        for key in ['InstanceCreateTime', 'Engine', 'DBInstanceStatus', 'AutoMinorVersionUpgrade',
                    'DBInstanceClass', 'MultiAZ', 'Endpoint', 'BackupRetentionPeriod', 'PubliclyAccessible',
                    'StorageEncrypted', 'VpcSecurityGroups', 'DBSecurityGroups', 'DBParameterGroups',
                    'EnhancedMonitoringResourceArn', 'StorageEncrypted', 'CACertificateIdentifier', 'Tags']:
            instance[key] = raw_instance[key] if key in raw_instance else None

        instance['is_read_replica'] = self._is_read_replica(raw_instance)
        instance['arn'] = raw_instance.get('DBInstanceArn')
        return instance['name'], instance

    @staticmethod
    def _is_read_replica(instance):
        # The ReadReplicaSourceDBInstanceIdentifier attribute is only defined for read replicas. Ref.: https://bit.ly/2UhKPqP
        return instance.get('ReadReplicaSourceDBInstanceIdentifier') is not None
