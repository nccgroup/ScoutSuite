from ScoutSuite.providers.azure.resources.base import AzureResources


class Users(AzureResources):
    async def fetch_all(self):
        for raw_user in await self.facade.aad.get_users():
            id, user = await self._parse_user(raw_user)
            self[id] = user

    async def fetch_additional_users(self, user_list):
        """
        Alternative method which only fetches defined users
        :param user_list: a list of the users to fetch and parse
        """
        for user in user_list:
            raw_user = await self.facade.aad.get_user(user)
            if raw_user:
                id, user = await self._parse_user(raw_user)
                self[id] = user

    async def _parse_user(self, raw_user):
        user_dict = {}
        user_dict['id'] = raw_user.get('id')
        # user_dict['additional_properties'] = raw_user.additional_properties
        user_dict['deletion_timestamp'] = raw_user.get('deletedDateTime')
        user_dict['object_type'] = 'User'
        # user_dict['immutable_id'] = raw_user.immutable_id
        user_dict['usage_location'] = raw_user.get('usageLocation')
        user_dict['given_name'] = raw_user.get('given_name')
        user_dict['surname'] = raw_user.get('surname')
        user_dict['user_type'] = raw_user.get('userType')
        user_dict['account_enabled'] = raw_user.get('accountEnabled')
        user_dict['display_name'] = raw_user.get('displayName')
        user_dict['name'] = raw_user.get('userPrincipalName')
        user_dict['mail_nickname'] = raw_user.get('mailNickname')
        user_dict['mail'] = raw_user.get('mail')
        # user_dict['sign_in_names'] = raw_user.sign_in_names
        user_dict['groups'] = await self.facade.aad.get_user_groups(user_dict['id'])
        user_dict['roles'] = []  # this will be filled in `finalize()`

        return user_dict['id'], user_dict
