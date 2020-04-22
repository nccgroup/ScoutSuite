from ScoutSuite.core.console import print_exception
from ScoutSuite.providers.aws.facade.basefacade import AWSBaseFacade
from ScoutSuite.providers.aws.facade.utils import AWSFacadeUtils


class SecretsManagerFacade(AWSBaseFacade):
    async def get_secrets(self, region):
        try:
            return await AWSFacadeUtils.get_all_pages('secretsmanager', region, self.session, 'list_secrets', 'SecretList')
        except Exception as e:
            print_exception('Failed to get Secrets Manager secrets: {}'.format(e))
            return []
