from ScoutSuite.providers.aws.facade.base import AWSFacade
from ScoutSuite.providers.aws.resources.base import AWSResources


class Aliases(AWSResources):
    def __init__(self, facade: AWSFacade, region: str):
        super(Aliases, self).__init__(facade)
        self.region = region

    async def fetch_all(self):
        raw_aliases = await self.facade.kms.get_aliases(self.region)
        for raw_alias in raw_aliases:
            id, alias = self._parse_alias(raw_alias)
            self[id] = alias

    def _parse_alias(self, raw_alias):
        alias_dict = {
            # all KMS Aliases are prefixed with alias/, so we'll strip that off
            'name': raw_alias.get('AliasName').lstrip('alias/'),
            'arn': raw_alias.get('AliasArn'),
            'key_id': raw_alias.get('TargetKeyId')}
        return alias_dict['name'], alias_dict
