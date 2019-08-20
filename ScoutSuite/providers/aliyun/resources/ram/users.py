from ScoutSuite.providers.aliyun.resources.base import AliyunCompositeResources

from .api_keys import ApiKeys


class Users(AliyunCompositeResources):
    _children = [
        (ApiKeys, 'api_keys')
    ]

    async def fetch_all(self):
        for raw_user in await self.facade.ram.get_users():
            id, user = await self._parse_user(raw_user)
            self[id] = user

        await self._fetch_children_of_all_resources(
            resources=self,
            scopes={user_id: {'user': user}
                    for user_id, user in self.items()}
        )

    async def _parse_user(self, raw_user):
        user = {}
        user['identifier'] = raw_user['UserId']  # required as groups use the name as an ID
        user['id'] = user['name'] = raw_user['UserName']
        user['display_name'] = raw_user['DisplayName']
        user['comments'] = raw_user['Comments']
        user['creation_datetime'] = raw_user['CreateDate']
        user['update_datetime'] = raw_user['CreateDate']
        user['creation_date'] = raw_user['CreateDate']

        # get additional details for the user
        user_details = await self.facade.ram.get_user_details(user['name'])
        user['email'] = user_details.get('Email')
        user['mobile_phone'] = user_details.get('MobilePhone')
        user['last_login_datetime'] = user_details.get('LastLoginDate') if user_details.get('LastLoginDate') != '' else None

        user['console_access'] = True if user_details.get('LastLoginDate') else False  # TODO this isn't valid

        # get the MFA status for the user
        mfa_enabled, mfa_serial_number = await self.facade.ram.get_user_mfa_status(user['name'])
        user['mfa_status'] = mfa_enabled
        user['mfa_serial_number'] = mfa_serial_number

        return user['id'], user
