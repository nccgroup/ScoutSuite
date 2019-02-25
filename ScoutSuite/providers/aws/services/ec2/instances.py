from ScoutSuite.providers.aws.resources.resources import AWSSimpleResources
from ScoutSuite.providers.aws.facade.facade import AWSFacade
from opinel.utils.aws import get_name
from ScoutSuite.utils import get_keys


class EC2Instances(AWSSimpleResources):
    async def get_resources_from_api(self):
        return self.facade.ec2.get_instances(self.scope['region'], self.scope['vpc'])
        
    def parse_resource(self, raw_instance):
        instance = {}
        id = raw_instance['InstanceId']
        instance['id'] = id
        instance['monitoring_enabled'] = raw_instance['Monitoring']['State'] == 'enabled'
        instance['user_data'] = self.facade.ec2.get_instance_user_data(self.scope['region'], id)

        # TODO: Those methods are slightly sketchy in my opinion (get methods which set stuff in a dictionary, say what)
        get_name(raw_instance, instance, 'InstanceId')
        get_keys(raw_instance, instance, ['KeyName', 'LaunchTime', 'InstanceType', 'State', 'IamInstanceProfile', 'SubnetId'])

        instance['network_interfaces'] = {}
        for eni in raw_instance['NetworkInterfaces']:
            nic = {}
            get_keys(eni, nic, ['Association', 'Groups', 'PrivateIpAddresses', 'SubnetId', 'Ipv6Addresses'])
            instance['network_interfaces'][eni['NetworkInterfaceId']] = nic

        return id, instance
