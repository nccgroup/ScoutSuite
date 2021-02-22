import json

from ScoutSuite.core.console import print_exception
from ScoutSuite.providers.aws.facade.basefacade import AWSBaseFacade
from ScoutSuite.providers.aws.facade.utils import AWSFacadeUtils
from ScoutSuite.providers.utils import map_concurrently, run_concurrently, get_and_set_concurrently


class SecretsManagerFacade(AWSBaseFacade):
    async def get_secrets(self, region):
        try:
            secrets_list = await AWSFacadeUtils.get_all_pages('secretsmanager', region, self.session,
                                                              'list_secrets', 'SecretList')
        except Exception as e:
            print_exception(f'Failed to get Secrets Manager secrets: {e}')
            return []
        else:
            secrets_list = await map_concurrently(self._describe_secrets, secrets_list, region=region)

            await get_and_set_concurrently(
                [
                    self._get_and_set_secret_policy
                ],
                secrets_list,
                region=region)

            return secrets_list

    async def _describe_secrets(self, secret: str, region: str):
        client = AWSFacadeUtils.get_client('secretsmanager', self.session, region)

        try:
            secret_description = await run_concurrently(lambda: client.describe_secret(SecretId=secret.get('ARN')))
        except Exception as e:
            print_exception('Failed to get Secrets Manager secret details: {}'.format(e))
            return secret
        else:
            secret_description.pop('ResponseMetadata')
            return secret_description

    async def _get_and_set_secret_policy(self, secret: {}, region: str):
        client = AWSFacadeUtils.get_client('secretsmanager', self.session, region)

        try:
            policy = await run_concurrently(lambda: client.get_resource_policy(SecretId=secret.get('ARN')))
            policy_json = policy.get('ResourcePolicy')
            if policy_json:
                secret['policy'] = json.loads(policy_json)
            else:
                secret['policy'] = {}
        except Exception as e:
            print_exception('Failed to get Secrets Manager secret policy: {}'.format(e))
            secret['policy'] = {}
