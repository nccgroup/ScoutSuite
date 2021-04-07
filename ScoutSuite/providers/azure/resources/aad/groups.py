from ScoutSuite.providers.azure.resources.base import AzureResources


class Groups(AzureResources):
    async def fetch_all(self):
        for raw_group in await self.facade.aad.get_groups():
            id, group = await self._parse_group(raw_group)
            self[id] = group

    async def _parse_group(self, raw_group):

        group_dict = {}

        group_dict['id'] = raw_group.get('id')
        group_dict['name'] = raw_group.get('displayName')
        # group_dict['additional_properties'] = raw_group.additional_properties
        group_dict['deletion_timestamp'] = raw_group.get('deletedDateTime')
        group_dict['object_type'] = 'Group'
        group_dict['mail_enabled'] = raw_group.get('mailEnabled')
        group_dict['mail_nickname'] = raw_group.get('mailNickname')
        group_dict['security_enabled'] = raw_group.get('securityEnabled')
        group_dict['mail'] = raw_group.get('mail')
        group_dict['users'] = []  # this will be filled in `finalize()`
        group_dict['roles'] = []  # this will be filled in `finalize()`

        return group_dict['id'], group_dict

