from ScoutSuite.providers.openstack.resources.base import OpenstackResources


class Users(OpenstackResources):
    async def fetch_all(self):
        raw_users = await self.facade.keystone.get_users()
        for raw_user in raw_users:
            id, user = self._parse_user(raw_user)
            if id in self:
                continue

            self[id] = user

    def _parse_user(self, raw_user):
        user_dict = {}
        user_dict['id'] = raw_user.id
        user_dict['name'] = raw_user.name
        user_dict['email'] = raw_user.email
        user_dict['description'] = raw_user.description
        user_dict['domain_id'] = raw_user.domain_id
        user_dict['enabled'] = raw_user.is_enabled
        user_dict['password_expires_at'] = raw_user.password_expires_at
        return user_dict['id'], user_dict


