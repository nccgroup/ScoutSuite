from ScoutSuite.providers.aws.resources.resources import AWSResources
from ScoutSuite.providers.aws.facade.facade import AWSFacade
from ScoutSuite.providers.aws.aws import get_name
from ScoutSuite.providers.aws.utils import ec2_classic, get_keys


class EC2Instances(AWSResources):
    async def fetch_all(self, **kwargs):
        raw_instances  = self.facade.ec2.get_instances(self.scope['region'], self.scope['vpc'])
        for raw_instance in raw_instances:
            name, resource = self._parse_instance(raw_instance)
            self[name] = resource

    def _parse_instance(self, raw_instance):
        instance = {}
        id = raw_instance['InstanceId']
        instance['id'] = id
        instance['reservation_id'] = raw_instance['ReservationId']
        instance['monitoring_enabled'] = raw_instance['Monitoring']['State'] == 'enabled'
        instance['user_data'] = self.facade.ec2.get_instance_user_data(self.scope['region'], id)

        get_name(raw_instance, instance, 'InstanceId')
        get_keys(raw_instance, instance, ['KeyName', 'LaunchTime', 'InstanceType', 'State', 'IamInstanceProfile', 'SubnetId'])

        instance['network_interfaces'] = {}
        for eni in raw_instance['NetworkInterfaces']:
            nic = {}
            get_keys(eni, nic, ['Association', 'Groups', 'PrivateIpAddresses', 'SubnetId', 'Ipv6Addresses'])
            instance['network_interfaces'][eni['NetworkInterfaceId']] = nic

        return id, instance
