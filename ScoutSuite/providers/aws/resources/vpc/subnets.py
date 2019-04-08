from ScoutSuite.providers.aws.resources.resources import AWSResources
from ScoutSuite.providers.aws.utils import get_name


class Subnets(AWSResources):
    async def fetch_all(self, **kwargs):
        raw_subnets = await self.facade.ec2.get_subnets(self.scope['region'], self.scope['vpc'])
        for raw_subnet in raw_subnets:
            id, subnet = self._parse_subnet(raw_subnet)
            self[id] = subnet

    def _parse_subnet(self, raw_subnet):
        raw_subnet['id'] = raw_subnet['SubnetId']
        get_name(raw_subnet, raw_subnet, 'SubnetId')
        raw_subnet.pop('SubnetId')

        return raw_subnet['id'], raw_subnet
