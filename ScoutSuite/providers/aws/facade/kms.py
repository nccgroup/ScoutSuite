from ScoutSuite.core.console import print_exception
from ScoutSuite.providers.aws.facade.basefacade import AWSBaseFacade
from ScoutSuite.providers.aws.facade.utils import AWSFacadeUtils


class KMSFacade(AWSBaseFacade):

    async def get_aliases(self):
        try:
            return await AWSFacadeUtils.get_all_pages('kms', None, self.session, 'list_aliases', 'Aliases')
        except Exception as e:
            print_exception('Failed to list KMS Aliases: {}'.format(e))
            return []

    async def get_grants(self):
        try:
            return await AWSFacadeUtils.get_all_pages('kms', None, self.session, 'list_grants', 'Grants')
        except Exception as e:
            print_exception('Failed to list KMS Grants: {}'.format(e))
            return []

    async def get_key_policies(self):
        try:
            return await AWSFacadeUtils.get_all_pages('kms', None, self.session, 'list_key_policies', 'PolicyNames')
        except Exception as e:
            print_exception('Failed to list KMS Key Policies: {}'.format(e))
            return []

    async def get_keys(self):
        try:
            return await AWSFacadeUtils.get_all_pages('kms', None, self.session, 'list_keys', 'Keys')
        except Exception as e:
            print_exception('Failed to list KMS Keys: {}'.format(e))
            return []
