from ScoutSuite.providers.aws.configs.regions_config import ScopedResources
from ScoutSuite.providers.aws.facade.facade import AWSFacade
from opinel.utils.aws import get_name
from ScoutSuite.utils import get_keys


class EC2Instances(ScopedResources):
    def __init__(self, region):
        self.region = region
        self.facade = AWSFacade()

    def parse_resource(self, raw_instance):
        instance = {}
        id = raw_instance['InstanceId']
        instance['id'] = id
        instance['monitoring_enabled'] = raw_instance['Monitoring']['State'] == 'enabled'
        instance['user_data'] = self.facade.ec2.get_instance_user_data(self.region, id)

        # TODO: Those methods are slightly sketchy in my opinion (get methods which set stuff in a dictionary, say what)
        get_name(raw_instance, instance, 'InstanceId')
        get_keys(raw_instance, instance, ['KeyName', 'LaunchTime', 'InstanceType', 'State', 'IamInstanceProfile', 'SubnetId'])

        instance['network_interfaces'] = {}
        for eni in raw_instance['NetworkInterfaces']:
            nic = {}
            get_keys(eni, nic, ['Association', 'Groups', 'PrivateIpAddresses', 'SubnetId', 'Ipv6Addresses'])
            instance['network_interfaces'][eni['NetworkInterfaceId']] = nic

        return id, instance

    async def get_resources_in_scope(self, vpcs): 
        return self.facade.ec2.get_instances(self.region, vpcs)