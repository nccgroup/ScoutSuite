from ScoutSuite.providers.ksyun.resources.base import KsyunCompositeResources

from .api_keys import ApiKeys


class Users(KsyunCompositeResources):
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
        user['display_name'] = raw_user['RealName']
        user['comments'] = raw_user['Remark']
        user['update_datetime'] = raw_user['UpdateDate']
        user['creation_date'] = raw_user['CreateDate']

        # get additional details for the user
        user_details = await self.facade.ram.get_user_details(user['name'])
        user['email'] = user_details.get('Email')
        user['mobile_phone'] = user_details.get('Phone')
        user['mfa_status'] = user_details.get('EnableMFA')
        # get the MFA status for the user
        mfa_serial_number = await self.facade.ram.get_user_mfa_status(user['name'])
        user['mfa_serial_number'] = mfa_serial_number

        return user['id'], user
