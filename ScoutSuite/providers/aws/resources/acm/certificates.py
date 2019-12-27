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

        certificate_dict = {}
        certificate_dict['CertificateArn'] = raw_certificate.get('CertificateArn')
        certificate_dict['DomainName'] = raw_certificate.get('DomainName')
        certificate_dict['Subject'] = raw_certificate.get('Subject')
        certificate_dict['Issuer'] = raw_certificate.get('Issuer')
        certificate_dict['Status'] = raw_certificate.get('Status')
        certificate_dict['RevokedReason'] = raw_certificate.get('RevokedReason')
        certificate_dict['KeyAlgorithm'] = raw_certificate.get('KeyAlgorithm')
        certificate_dict['FailureReason'] = raw_certificate.get('FailureReason')
        certificate_dict['CertificateAuthorityArn'] = raw_certificate.get('CertificateAuthorityArn')
        certificate_dict['CertificateTransparencyLoggingPreference'] = raw_certificate.get('Options').get('CertificateTransparencyLoggingPreference')

        return certificate_dict['CertificateArn'], certificate_dict

