from ScoutSuite.providers.aws.facade.base import AWSFacade
from ScoutSuite.providers.aws.resources.base import AWSResources
from ScoutSuite.core.console import print_exception


class Snapshots(AWSResources):
    def __init__(self, facade: AWSFacade, region: str, vpc: str):
        super().__init__(facade)
        self.region = region
        self.vpc = vpc

    async def fetch_all(self):
        raw_snapshots = await self.facade.rds.get_snapshots(self.region, self.vpc)
        parsing_error_counter = 0
        for raw_snapshot in raw_snapshots:
            try:
                name, resource = self._parse_snapshot(raw_snapshot)
                self[name] = resource
            except Exception as e:
                parsing_error_counter += 1
        if parsing_error_counter > 0:
            print_exception(
                'Failed to parse {} resource: {} times'.format(self.__class__.__name__, parsing_error_counter))

    def _parse_snapshot(self, raw_snapshot):
        is_cluster = 'DBClusterIdentifier' in raw_snapshot

        snapshot_id = raw_snapshot.pop('DBClusterSnapshotIdentifier') if is_cluster \
            else raw_snapshot.pop('DBSnapshotIdentifier')

        snapshot = {}
        snapshot['arn'] = raw_snapshot.pop('DBClusterSnapshotArn') if is_cluster else raw_snapshot.pop('DBSnapshotArn')
        snapshot['id'] = snapshot_id,
        snapshot['name'] = snapshot_id,
        snapshot['vpc_id'] = raw_snapshot['VpcId']
        snapshot['attributes'] = raw_snapshot['Attributes']
        snapshot['is_cluster'] = is_cluster

        attributes = [
            'DBInstanceIdentifier',
            'SnapshotCreateTime',
            'Encrypted',
            'OptionGroupName'
        ]
        for attribute in attributes:
            snapshot[attribute] = raw_snapshot[attribute] if attribute in raw_snapshot else None

        if snapshot['is_cluster']:  # Map some fields to do more generic and simple rules
            snapshot['DBClusterIdentifier'] = raw_snapshot['DBClusterIdentifier']
            snapshot['Encrypted'] = raw_snapshot['StorageEncrypted']

        return snapshot_id, snapshot
