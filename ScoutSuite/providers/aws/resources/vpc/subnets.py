from ScoutSuite.providers.aws.facade.base import AWSFacade
from ScoutSuite.providers.aws.resources.base import AWSResources
from ScoutSuite.providers.aws.utils import get_name
from ScoutSuite.core.console import print_exception


class Subnets(AWSResources):
    def __init__(self, facade: AWSFacade, region: str, vpc: str):
        self.region = region
        self.vpc = vpc

        super().__init__(facade)

    async def fetch_all(self):
        raw_subnets = await self.facade.ec2.get_subnets(self.region, self.vpc)
        for raw_subnet in raw_subnets:
            try:
                id, subnet = self._parse_subnet(raw_subnet)
                self[id] = subnet
            except Exception as e:
                print_exception('Failed to parse {} resource: {}'.format(self.__class__.__name__, e))

    def _parse_subnet(self, raw_subnet):
        raw_subnet['id'] = raw_subnet['SubnetId']
        get_name(raw_subnet, raw_subnet, 'SubnetId')
        raw_subnet.pop('SubnetId')

        if raw_subnet['Ipv6CidrBlockAssociationSet']:
            raw_subnet['CidrBlockv6'] = raw_subnet['Ipv6CidrBlockAssociationSet'][0]['Ipv6CidrBlock']
        else:
            raw_subnet['CidrBlockv6'] = None

        return raw_subnet['id'], raw_subnet
