from ScoutSuite.providers.azure.resources.base import AzureResources
from ScoutSuite.core.console import print_exception


class Groups(AzureResources):
    async def fetch_all(self):
        parsing_error_counter = 0
        for raw_group in await self.facade.aad.get_groups():
            try:
                id, group = await self._parse_group(raw_group)
                self[id] = group
            except Exception as e:
                parsing_error_counter += 1
        if parsing_error_counter > 0:
            print_exception(
                'Failed to parse {} resource: {} times'.format(self.__class__.__name__, parsing_error_counter))

    async def _parse_group(self, raw_group):

        group_dict = {}

        group_dict['id'] = raw_group.object_id
        group_dict['name'] = raw_group.display_name
        group_dict['additional_properties'] = raw_group.additional_properties
        group_dict['deletion_timestamp'] = raw_group.deletion_timestamp
        group_dict['object_type'] = raw_group.object_type
        group_dict['mail_enabled'] = raw_group.mail_enabled
        group_dict['mail_nickname'] = raw_group.mail_nickname
        group_dict['security_enabled'] = raw_group.security_enabled
        group_dict['mail'] = raw_group.mail
        group_dict['users'] = []  # this will be filled in `finalize()`
        group_dict['roles'] = []  # this will be filled in `finalize()`

        return group_dict['id'], group_dict

