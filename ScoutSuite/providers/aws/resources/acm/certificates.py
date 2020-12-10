from ScoutSuite.providers.aws.facade.base import AWSFacade
from ScoutSuite.providers.aws.resources.base import AWSResources

from ScoutSuite.providers.utils import get_non_provider_id


class Certificates(AWSResources):
    def __init__(self, facade: AWSFacade, region: str):
        super().__init__(facade)
        self.region = region

    async def fetch_all(self):
        raw_certificates = await self.facade.acm.get_certificates(self.region)
        for raw_certificate in raw_certificates:
            name, resource = self._parse_certificate(raw_certificate)
            self[name] = resource

    def _parse_certificate(self, raw_certificate):
        raw_certificate['name'] = raw_certificate.get('DomainName')
        raw_certificate['id'] = get_non_provider_id(raw_certificate['name'])
        raw_certificate['arn'] = raw_certificate.get('DomainName')

        return raw_certificate['id'], raw_certificate
