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

        certificate_dict['certificate_arn'] = raw_certificate.get('CertificateArn')
        certificate_dict['domain_name'] = raw_certificate.get('DomainName')
        certificate_dict['subject_alternative_names'] = raw_certificate.get('SubjectAlternativeNames')
        certificate_dict['domain_validation_options'] = raw_certificate.get('DomainValidationOptions')
        certificate_dict['subject'] = raw_certificate.get('Subject')
        certificate_dict['issuer'] = raw_certificate.get('Issuer')
        certificate_dict['created_at'] = raw_certificate.get('CreatedAt')
        certificate_dict['status'] = raw_certificate.get('Status')
        certificate_dict['key_algorithm'] = raw_certificate.get('KeyAlgorithm')
        certificate_dict['signature_algorithm'] = raw_certificate.get('SignatureAlgorithm')
        certificate_dict['in_use_by'] = raw_certificate.get('InUseBy')
        certificate_dict['type'] = raw_certificate.get('Type')
        certificate_dict['key_usages'] = raw_certificate.get('KeyUsages')
        certificate_dict['extended_key_usages'] = raw_certificate.get('ExtendedKeyUsages')
        certificate_dict['renewal_eligibility'] = raw_certificate.get('RenewalEligibility')
        certificate_dict['options'] = raw_certificate.get('Options')
        certificate_dict['name'] = raw_certificate.get('DomainName')

        return certificate_dict['name'], certificate_dict
