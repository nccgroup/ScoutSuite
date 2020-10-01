from ScoutSuite.core.console import print_exception
from ScoutSuite.providers.aws.facade.basefacade import AWSBaseFacade
from ScoutSuite.providers.aws.facade.utils import AWSFacadeUtils
from ScoutSuite.providers.utils import run_concurrently, get_and_set_concurrently
import json



class KMSFacade(AWSBaseFacade):

    async def get_keys(self, region: str):

        try:
            keys = await AWSFacadeUtils.get_all_pages('kms', region, self.session, 'list_keys', 'Keys')
            await get_and_set_concurrently(
                [self._get_and_set_key_policy,
                 self._get_and_set_key_metadata,
                 self._get_and_set_key_aliases],
                keys, region=region)
        except Exception as e:
            print_exception(f'Failed to get KMS keys: {e}')
            keys = []
        finally:
            return keys

    async def _get_and_set_key_policy(self, key: {}, region: str):
        client = AWSFacadeUtils.get_client('kms', self.session, region)
        try:
            response = await run_concurrently(
                lambda: client.get_key_policy(KeyId=key['KeyId'],
                                              PolicyName='default'))
            key['policy'] = json.loads(response.get('Policy'))
        except Exception as e:
            print_exception(f'Failed to get KMS key policy: {e}')

    async def _get_and_set_key_metadata(self, key: {}, region: str):
        client = AWSFacadeUtils.get_client('kms', self.session, region)
        try:
            key['metadata'] = await run_concurrently(lambda: client.describe_key(KeyId=key['KeyId']))
        except Exception as e:
            print_exception(f'Failed to describe KMS key: {e}')

    async def _get_and_set_key_aliases(self, key: {}, region: str):
        client = AWSFacadeUtils.get_client('kms', self.session, region)
        try:
            response = await run_concurrently(
                lambda: client.list_aliases(KeyId=key['KeyId'])
            )
            key['aliases'] = response.get('Aliases')
        except Exception as e:
            print_exception(f'Failed to get KMS aliases: {e}')

    async def get_grants(self, region: str, key_id: str):
        try:
            return await AWSFacadeUtils.get_all_pages('kms', region, self.session, 'list_grants', 'Grants',
                                                      KeyId=key_id)
        except Exception as e:
            print_exception(f'Failed to list KMS Grants: {e}')
            return []

    async def get_key_rotation_status(self, region: str, key_id: str):
        client = AWSFacadeUtils.get_client('kms', self.session, region)
        try:
            return await run_concurrently(
                lambda: client.get_key_rotation_status(KeyId=key_id))
        except Exception as e:
            print_exception(f'Failed to get KMS key rotation: {e}')
