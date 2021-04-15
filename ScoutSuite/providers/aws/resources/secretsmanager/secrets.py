from ScoutSuite.providers.aws.facade.base import AWSFacade
from ScoutSuite.providers.aws.resources.base import AWSResources
from ScoutSuite.providers.utils import get_non_provider_id


class Secrets(AWSResources):
    def __init__(self, facade: AWSFacade, region: str):
        super().__init__(facade)
        self.region = region

    async def fetch_all(self):
        for raw_secret in await self.facade.secretsmanager.get_secrets(self.region):
            id, secret = self._parse_secret(raw_secret)
            self[id] = secret

    def _parse_secret(self, raw_secret):
        secret_dict = {}
        secret_dict['id'] = get_non_provider_id(raw_secret.get('ARN'))
        secret_dict['arn'] = raw_secret.get('ARN')
        secret_dict['name'] = raw_secret.get('Name')
        secret_dict['description'] = raw_secret.get('Description')
        secret_dict['last_changed_date'] = raw_secret.get('LastChangedDate')
        secret_dict['last_accessed_date'] = raw_secret.get('LastAccessedDate')
        secret_dict['tags'] = raw_secret.get('Tags')
        secret_dict['secret_versions_to_stages'] = raw_secret.get('SecretVersionsToStages')
        secret_dict['kms'] = raw_secret.get('KmsKeyId')
        secret_dict['policy'] = raw_secret.get('policy')
        secret_dict['rotation'] = raw_secret.get('RotationEnabled', False)
        secret_dict['rotation_lambda_arn'] = raw_secret.get('RotationLambdaARN')
        secret_dict['rotation_interval'] = raw_secret.get('RotationRules', {}).get('AutomaticallyAfterDays')
        return secret_dict['id'], secret_dict
