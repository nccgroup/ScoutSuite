from ScoutSuite.providers.aws.facade.base import AWSFacade
from ScoutSuite.providers.aws.resources.base import AWSResources


class Certificates(AWSResources):
    def __init__(self, facade: AWSFacade, region: str):
        super(Certificates, self).__init__(facade)
        self.region = region

    async def fetch_all(self):
        raw_certificates = await self.facade.acm.get_certificates(self.region)
        for raw_certificate in raw_certificates:
            name, resource = self._parse_certificate(raw_certificate)
            self[name] = resource

    def _parse_certificate(self, raw_certificate):
        raw_certificate['name'] = raw_certificate['CertificateArn']
        raw_certificate['arn'] = raw_certificate['CertificateArn']

        return raw_certificate.get('CertificateArn'), raw_certificate

