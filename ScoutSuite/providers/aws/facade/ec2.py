import asyncio
import base64
import boto3
import zlib

from ScoutSuite.core.console import print_exception
from ScoutSuite.providers.aws.facade.basefacade import AWSBaseFacade
from ScoutSuite.providers.aws.facade.utils import AWSFacadeUtils
from ScoutSuite.providers.utils import get_and_set_concurrently
from ScoutSuite.providers.utils import run_concurrently


class EC2Facade(AWSBaseFacade):
    regional_flow_logs_cache_locks = {}
    flow_logs_cache = {}

    def __init__(self, session: boto3.session.Session, owner_id: str):
        self.owner_id = owner_id

        super().__init__(session)

    async def get_instance_user_data(self, region: str, instance_id: str):
        ec2_client = AWSFacadeUtils.get_client('ec2', self.session, region)
        try:
            user_data_response = await run_concurrently(
                lambda: ec2_client.describe_instance_attribute(Attribute='userData', InstanceId=instance_id))
        except Exception as e:
            print_exception(
                f'Failed to describe EC2 instance attributes: {e}')
            return None
        else:
            if 'Value' not in user_data_response['UserData'].keys():
                return None
            else:
                try:
                    return await self._decode_user_data(user_data_response['UserData']['Value'])
                except base64.binascii.Error as e:
                    return await self._decode_user_data(base64.b64decode(user_data_response['UserData']['Value'] + "==="))
                except Exception as e:
                    print_exception(f'Unable to decode EC2 instance user data: {e}')

    async def _decode_user_data(self, user_data):
        value = base64.b64decode(user_data)
        if value[0:2] == b'\x1f\x8b':  # GZIP magic number
            return zlib.decompress(value, zlib.MAX_WBITS | 32).decode('utf-8')
        else:
            return value.decode('utf-8')

    async def get_instances(self, region: str, vpc: str):
        filters = [{'Name': 'vpc-id', 'Values': [vpc]}]
        try:
            reservations = \
                await AWSFacadeUtils.get_all_pages(
                    'ec2', region, self.session, 'describe_instances', 'Reservations', Filters=filters)

            instances = []
            for reservation in reservations:
                for instance in reservation['Instances']:
                    instance['ReservationId'] = reservation['ReservationId']
                    instance['OwnerId'] = reservation['OwnerId']
                    instances.append(instance)
            return instances
        except Exception as e:
            print_exception(f'Failed to describe EC2 instances: {e}')
            return []

    async def get_security_groups(self, region: str, vpc: str):
        filters = [{'Name': 'vpc-id', 'Values': [vpc]}]
        try:
            return await AWSFacadeUtils.get_all_pages(
                'ec2', region, self.session, 'describe_security_groups', 'SecurityGroups', Filters=filters)
        except Exception as e:
            print_exception(f'Failed to describe EC2 security groups: {e}')
            return []

    async def get_vpcs(self, region: str):
        ec2_client = AWSFacadeUtils.get_client('ec2', self.session, region)
        try:
            return await run_concurrently(lambda: ec2_client.describe_vpcs()['Vpcs'])
        except Exception as e:
            print_exception(f'Failed to describe EC2 VPC: {e}')
            return []

    async def get_images(self, region: str):
        filters = [{'Name': 'owner-id', 'Values': [self.owner_id]}]
        client = AWSFacadeUtils.get_client('ec2', self.session, region)
        try:
            return await run_concurrently(lambda: client.describe_images(Filters=filters)['Images'])
        except Exception as e:
            print_exception(f'Failed to get EC2 images: {e}')
            return []

    async def get_network_interfaces(self, region: str, vpc: str):
        filters = [{'Name': 'vpc-id', 'Values': [vpc]}]
        try:
            return await AWSFacadeUtils.get_all_pages(
                'ec2', region, self.session, 'describe_network_interfaces', 'NetworkInterfaces', Filters=filters)
        except Exception as e:
            print_exception(f'Failed to get EC2 network interfaces: {e}')
            return []

    async def get_volumes(self, region: str):
        try:
            volumes = await AWSFacadeUtils.get_all_pages('ec2', region, self.session, 'describe_volumes', 'Volumes')
            await get_and_set_concurrently([self._get_and_set_key_manager, self._get_and_set_volume_tags], volumes, region=region)
            return volumes
        except Exception as e:
            print_exception(f'Failed to get EC2 volumes: {e}')
            return []

    async def _get_and_set_volume_tags(self, volume: {}, region: str):
        if "Tags" in volume:
            volume["tags"] = {x["Key"]: x["Value"] for x in volume["Tags"]}
        else:
            volume["tags"] = {}
        return volume

    async def _get_and_set_key_manager(self, volume: {}, region: str):
        kms_client = AWSFacadeUtils.get_client('kms', self.session, region)
        if 'KmsKeyId' in volume:
            key_id = volume['KmsKeyId']
            try:
                volume['KeyManager'] = await run_concurrently(
                    lambda: kms_client.describe_key(KeyId=key_id)['KeyMetadata']['KeyManager'])
            except Exception as e:
                print_exception(f'Failed to describe KMS key: {e}')
                volume['KeyManager'] = None
        else:
            volume['KeyManager'] = None

    async def get_snapshots(self, region: str):
        filters = [{'Name': 'owner-id', 'Values': [self.owner_id]}]

        try:
            snapshots = await AWSFacadeUtils.get_all_pages(
                'ec2', region, self.session, 'describe_snapshots', 'Snapshots', Filters=filters)
        except Exception as e:
            print_exception(f'Failed to get snapshots: {e}')
            snapshots = []
        else:
            await get_and_set_concurrently([self._get_and_set_snapshot_attributes], snapshots, region=region)
        finally:
            return snapshots

    async def _get_and_set_snapshot_attributes(self, snapshot: {}, region: str):
        ec2_client = AWSFacadeUtils.get_client('ec2', self.session, region)
        try:
            snapshot['CreateVolumePermissions'] = await run_concurrently(lambda: ec2_client.describe_snapshot_attribute(
                Attribute='createVolumePermission',
                SnapshotId=snapshot['SnapshotId'])['CreateVolumePermissions'])
        except Exception as e:
            print_exception(
                f'Failed to describe EC2 snapshot attributes: {e}')

    async def get_network_acls(self, region: str, vpc: str):
        filters = [{'Name': 'vpc-id', 'Values': [vpc]}]
        try:
            return await AWSFacadeUtils.get_all_pages(
                'ec2', region, self.session, 'describe_network_acls', 'NetworkAcls', Filters=filters)
        except Exception as e:
            print_exception(f'Failed to get EC2 network ACLs: {e}')
            return []

    async def get_flow_logs(self, region: str):
        try:
            await self.cache_flow_logs(region)
            return self.flow_logs_cache[region]
        except Exception as e:
            print_exception(f'Failed to get EC2 flow logs: {e}')
            return []

    async def cache_flow_logs(self, region: str):
        async with self.regional_flow_logs_cache_locks.setdefault(region, asyncio.Lock()):
            if region in self.flow_logs_cache:
                return

            self.flow_logs_cache[region] = \
                await AWSFacadeUtils.get_all_pages('ec2', region, self.session, 'describe_flow_logs', 'FlowLogs')

    async def get_subnets(self, region: str, vpc: str):
        ec2_client = AWSFacadeUtils.get_client('ec2', self.session, region)
        filters = [{'Name': 'vpc-id', 'Values': [vpc]}]
        try:
            subnets = await run_concurrently(lambda: ec2_client.describe_subnets(Filters=filters)['Subnets'])
        except Exception as e:
            print_exception(f'Failed to describe EC2 subnets: {e}')
            return None
        else:
            await get_and_set_concurrently([self._get_and_set_subnet_flow_logs], subnets, region=region)
            return subnets

    async def _get_and_set_subnet_flow_logs(self, subnet: {}, region: str):
        await self.cache_flow_logs(region)
        subnet['flow_logs'] = \
            [flow_log for flow_log in self.flow_logs_cache[region]
             if flow_log['ResourceId'] == subnet['SubnetId'] or flow_log['ResourceId'] == subnet['VpcId']]

    async def get_and_set_ec2_instance_tags(self, raw_instance: {}):
        if 'Tags' in raw_instance:
            instance = {x['Key']: x['Value'] for x in raw_instance['Tags']}
        else:
            instance = {}
        return instance

    async def get_peering_connections(self, region):
        try:
            peering_connections = await AWSFacadeUtils.get_all_pages('ec2', region, self.session, 'describe_vpc_peering_connections', 'VpcPeeringConnections')
            return peering_connections
        except Exception as e:
            print_exception(f'Failed to get peering connections: {e}')
            return []

    async def get_route_tables(self, region):
        try:
            route_tables = await AWSFacadeUtils.get_all_pages('ec2', region, self.session, 'describe_route_tables', 'RouteTables')
            return route_tables
        except Exception as e:
            print_exception('Failed to get route tables: {}'.format(e))
            return []