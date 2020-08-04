import abc

from ScoutSuite.providers.osc.resources.base import OSCCompositeResources
from ScoutSuite.providers.osc.facade.base import OSCFacade
import logging

class Regions(OSCCompositeResources, metaclass=abc.ABCMeta):

    def __init__(self, service: str, facade: OSCFacade):
        super(Regions, self).__init__(facade)
        self.service = service

    async def fetch_all(self, regions=None, excluded_regions=None, **kwargs):
        try:
            self['regions'] = {}
            for region in await self.facade.build_region_list(regions, excluded_regions):
                self['regions'][region['RegionName']] = {
                    'id': region['RegionName'],
                    'region': region,
                    'name': region['RegionName'],
                    'endpoint': region['Endpoint']
                }
            await self._fetch_children_of_all_resources(
                resources=self['regions'],
                scopes={region: {'region': region} for region in self['regions']}
            )
            self._set_counts()
        except Exception as e:
            logging.getLogger("scout").critical(f"OSC ::: Regions _fetch_all() Exception ::: {e}")


    def _set_counts(self):
        self['regions_count'] = len(self['regions'])

        for _, key in self._children:
            if key == 'vpcs':
                continue

            self[key + '_count'] = sum([region[key + '_count'] for region in self['regions'].values()])