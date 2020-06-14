from ScoutSuite.providers.salesforce.resources.base import SalesforceResources
from ScoutSuite.providers.salesforce.facade.base import SalesforceFacade


class Profiles(SalesforceResources):
    def __init__(self, facade: SalesforceFacade):
        super(Profiles, self).__init__(facade)

    async def fetch_all(self):
        for raw_profile in await self.facade.profiles.get_profiles():
            id, profile = await self._parse_profile(raw_profile)
            self[id] = profile

    async def _parse_profile(self, raw_profile):
        profile_dict = {}
        profile_dict['attributes'] = raw_profile.get('attributes')
        profile_dict['id'] = raw_profile.get('Id')
        profile_dict['name'] = raw_profile.get('Name')
        profile_dict['full_name'] = await self.facade.profiles.get_profile_full_name(profile_dict['id'])
        profile_dict['permissions_api_enabled'] = raw_profile.get('PermissionsApiEnabled')
        profile_dict['permissions_apex_rest_services'] = raw_profile.get('PermissionsApexRestServices')

        profile_dict['login_ip_ranges'] = \
            await self.facade.profiles.get_profile_login_restrictions(profile_dict['full_name'])

        return profile_dict['id'], profile_dict


