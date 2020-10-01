from ScoutSuite.providers.aws.resources.base import AWSResources
from ScoutSuite.providers.aws.facade.base import AWSFacade
from ScoutSuite.providers.aws.utils import get_name
from ScoutSuite.providers.aws.utils import get_keys
from ScoutSuite.providers.aws.utils import set_tags
import re


class EC2Instances(AWSResources):
    def __init__(self, facade: AWSFacade, region: str, vpc: str):
        super().__init__(facade)
        self.region = region
        self.vpc = vpc

    async def fetch_all(self):
        raw_instances = await self.facade.ec2.get_instances(self.region, self.vpc)
        for raw_instance in raw_instances:
            name, resource = await self._parse_instance(raw_instance)
            self[name] = resource

    async def _parse_instance(self, raw_instance):
        instance = {}
        id = raw_instance['InstanceId']
        instance['id'] = id
        instance['arn'] = 'arn:aws:ec2:{}.{}.instance/{}'.format(self.region,
                                                                raw_instance['OwnerId'],
                                                                raw_instance['InstanceId'])
        instance['reservation_id'] = raw_instance['ReservationId']
        instance['monitoring_enabled'] = raw_instance['Monitoring']['State'] == 'enabled'
        instance['user_data'] = await self.facade.ec2.get_instance_user_data(self.region, id)
        instance['user_data_secrets'] = self._identify_user_data_secrets(instance['user_data'])

        get_name(raw_instance, instance, 'InstanceId')
        get_keys(raw_instance, instance,
                 ['KeyName', 'LaunchTime', 'InstanceType', 'State', 'IamInstanceProfile', 'SubnetId', 'Tags'])

        if "IamInstanceProfile" in raw_instance:
            instance['iam_instance_profile_id'] = raw_instance['IamInstanceProfile']['Id']
            instance['iam_instance_profile_arn'] = raw_instance['IamInstanceProfile']['Arn']
        
        instance['network_interfaces'] = {}
        for eni in raw_instance['NetworkInterfaces']:
            nic = {}
            get_keys(eni, nic, ['Association', 'Groups', 'PrivateIpAddresses', 'SubnetId', 'Ipv6Addresses'])
            instance['network_interfaces'][eni['NetworkInterfaceId']] = nic

        instance['metadata_options'] = raw_instance['MetadataOptions']


        if 'IamInstanceProfile' in raw_instance:
            instance['iam_role'] = raw_instance['IamInstanceProfile']['Arn'].split('/')[-1]
        else:
            instance['iam_role'] = None

        instance['tags'] = await set_tags(raw_instance)
        
        return id, instance

    @staticmethod
    def _identify_user_data_secrets(user_data):
        """
        Parses EC2 user data in order to identify secrets and credentials..
        """
        secrets = {}

        if user_data:
            aws_access_key_regex = re.compile('AKIA[0-9A-Z]{16}')
            aws_secret_access_key_regex = re.compile('[0-9a-zA-Z/+]{40}')
            rsa_private_key_regex = re.compile('(-----BEGIN RSA PRIVATE KEY-----(?s).+?-----END .+?-----)')
            keywords = ['password', 'secret', 'aws_access_key_id', 'aws_secret_access_key', 'aws_session_token']

            aws_access_key_list = aws_access_key_regex.findall(user_data)
            if aws_access_key_list:
                secrets['AWS Access Key IDs'] = aws_access_key_list
            aws_secret_access_key_list = aws_secret_access_key_regex.findall(user_data)
            if aws_secret_access_key_list:
                secrets['AWS Secret Access Keys'] = aws_secret_access_key_list
            rsa_private_key_list = rsa_private_key_regex.findall(user_data)
            if rsa_private_key_list:
                secrets['Private Keys'] = rsa_private_key_list
            word_list = []
            for word in keywords:
                if word in user_data.lower():
                    word_list.append(word)
            if word_list:
                secrets['Flagged Words'] = word_list

        return secrets
