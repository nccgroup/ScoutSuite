from ScoutSuite.providers.aws.facade.base import AWSFacade
from ScoutSuite.providers.aws.resources.base import AWSResources


class Snapshots(AWSResources):
    def __init__(self, facade: AWSFacade, region: str, vpc: str):
        super().__init__(facade)
        self.region = region
        self.vpc = vpc

    async def fetch_all(self):
        raw_snapshots = await self.facade.rds.get_snapshots(self.region, self.vpc)
        for raw_snapshot in raw_snapshots:
            name, resource = self._parse_snapshot(raw_snapshot)
            self[name] = resource

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
