from ScoutSuite.core.console import print_exception
from ScoutSuite.providers.aws.facade.basefacade import AWSBaseFacade
from ScoutSuite.providers.aws.facade.utils import AWSFacadeUtils


class AcmFacade(AWSBaseFacade):
    async def get_certificates(self, region: str):
        try:
            certificates = await AWSFacadeUtils.get_all_pages('acm', region, self.session, 'list_certificates', 'CertificateSummaryList')
        except Exception as e:
            print_exception('Failed to get ACM certificates: {}'.format(e))
            certificates= []
        else:
            await get_and_set_concurrently( [self._get_and_set_certificate], certificates, region=region)
        finally:
            return certificates

    async def _get_and_set_certificate(self, certificate: {}, region: str):
        client = AWSFacadeUtils.get_client('acm', self.session, region)
        try:
            certificate_description = await run_concurrently(
                lambda: client.describe_certificate(CertificateArn=stack['CertificateArn'])['Certificate'])
        except Exception as e:
            print_exception('Failed to describe certificate: {}'.format(e))
        else:
            certificate.update(certificate_description)

