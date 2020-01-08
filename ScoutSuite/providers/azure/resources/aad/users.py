from ScoutSuite.providers.azure.resources.base import AzureResources


class Users(AzureResources):
    async def fetch_all(self):
        for raw_user in await self.facade.aad.get_users():
            id, user = await self._parse_user(raw_user)
            self[id] = user

    async def _parse_user(self, raw_user):
        user_dict = {}
        user_dict['id'] = raw_user.object_id
        user_dict['additional_properties'] = raw_user.additional_properties
        user_dict['deletion_timestamp'] = raw_user.deletion_timestamp
        user_dict['object_type'] = raw_user.object_type
        user_dict['immutable_id'] = raw_user.immutable_id
        user_dict['usage_location'] = raw_user.usage_location
        user_dict['given_name'] = raw_user.given_name
        user_dict['surname'] = raw_user.surname
        user_dict['user_type'] = raw_user.user_type
        user_dict['account_enabled'] = raw_user.account_enabled
        user_dict['display_name'] = raw_user.display_name
        user_dict['name'] = raw_user.user_principal_name
        user_dict['mail_nickname'] = raw_user.mail_nickname
        user_dict['mail'] = raw_user.mail
        user_dict['sign_in_names'] = raw_user.sign_in_names
        user_dict['user_type'] = raw_user.user_type
        user_dict['groups'] = await self.facade.aad.get_user_groups(user_dict['id'])
        user_dict['roles'] = []  # this will be filled in `finalize()`

        return user_dict['id'], user_dict
