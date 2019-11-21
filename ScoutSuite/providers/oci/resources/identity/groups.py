from ScoutSuite.providers.oci.resources.base import OracleResources
from ScoutSuite.providers.oci.facade.base import OracleFacade
from ScoutSuite.providers.utils import get_non_provider_id


class Groups(OracleResources):
    def __init__(self, facade: OracleFacade):
        super(Groups, self).__init__(facade)

    async def fetch_all(self):
        for raw_group in await self.facade.identity.get_groups():
            id, group = await self._parse_group(raw_group)
            self[id] = group

    async def _parse_group(self, raw_group):
        group_dict = {}
        group_dict['identifier'] = raw_group.id
        group_dict['id'] = get_non_provider_id(raw_group.id)
        group_dict['name'] = raw_group.name
        group_dict['lifecycle_state'] = raw_group.lifecycle_state
        group_dict['inactive_status'] = raw_group.inactive_status
        group_dict['description'] = raw_group.description
        group_dict['compartment_id'] = raw_group.compartment_id
        group_dict['time_created'] = raw_group.time_created
        group_dict['defined_tags'] = list(raw_group.defined_tags)
        group_dict['freeform_tags'] = list(raw_group.freeform_tags)

        members = await self.facade.identity.get_group_users(group_dict['identifier'])
        group_dict['users'] = []
        for member in members:
            member_dict = {}
            member_dict['user_identifier'] = member.user_id
            member_dict['user_id'] = get_non_provider_id(member.user_id)
            member_dict['membership_id'] = member.id
            member_dict['group_id'] = member.group_id
            member_dict['lifecycle_state'] = member.lifecycle_state
            member_dict['inactive_status'] = member.inactive_status
            member_dict['compartment_id'] = member.compartment_id
            member_dict['time_created'] = member.time_created
            group_dict['users'].append(member_dict)

        return group_dict['id'], group_dict



