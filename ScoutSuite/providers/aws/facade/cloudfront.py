import asyncio

from ScoutSuite.core.console import print_exception
from ScoutSuite.providers.aws.facade.basefacade import AWSBaseFacade
from ScoutSuite.providers.aws.facade.utils import AWSFacadeUtils
from ScoutSuite.providers.utils import run_concurrently

class CloudFront(AWSBaseFacade):

    async def get_distributions(self):
        client = AWSFacadeUtils.get_client('cloudfront',self.session)
        # When no cloudfront distribution exists, we first need to initiate the creation
        # of a new distributions generate_credential_report by calling
        # client.list_distributions and then check for COMPLETE status before trying to download it:
        aws_cloudfront_api_called, n_attempts = False, 3
        try:
            while not aws_cloudfront_api_called and n_attempts > 0:
                response = await run_concurrently(client.list_distributions)
                if 'ResponseMetadata' in response:
                    aws_cloudfront_api_called = True
                else:
                    n_attempts -= 1
                    await asyncio.sleep(0.1)  # Wait for 100ms before doing a new attempt.
        except Exception as e:
            print_exception('Failed to call aws cloudfront api: {}'.format(e))
            return []
        finally:
            if not aws_cloudfront_api_called and n_attempts == 0:
                print_exception('Failed to call aws cloudfront api in {} attempts'.format(n_attempts))
                return []

        try:
            return response.get('DistributionList', {}).get('Items', [])
        except Exception as e:
            print_exception(f'Failed to get CloudFront distribution lists: {e}')
            return []
