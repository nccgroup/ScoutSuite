import json

from ScoutSuite.providers.aws.facade.base import AWSFacade
from ScoutSuite.providers.aws.resources.base import AWSResources


class Secrets(AWSResources):
    def __init__(self, facade: AWSFacade, region: str):
        super(Secrets, self).__init__(facade)
        self.region = region

    async def fetch_all(self):
        for raw_secret in await self.facade.secretsmanager.get_secrets(self.region):
            id, secret = self._parse_secret(raw_secret)
            self[id] = secret

    def _parse_secret(self, raw_secret):
        secret_dict = {}
        secret_dict['arn'] = secret_dict['id'] = raw_secret.get('ARN')
        secret_dict['name'] = raw_secret.get('Name')
        secret_dict['description'] = raw_secret.get('Description')
        secret_dict['last_changed_date'] = raw_secret.get('LastChangedDate')
        secret_dict['tags'] = raw_secret.get('Tags')
        secret_dict['secret_versions_to_stages'] = raw_secret.get('SecretVersionsToStages')
        return secret_dict['id'], secret_dict

