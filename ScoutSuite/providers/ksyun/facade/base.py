import json

import requests
from collections import Counter
from ScoutSuite.providers.ksyun.facade.kec import KECFacade
from ScoutSuite.providers.ksyun.facade.ram import RAMFacade
from ScoutSuite.providers.ksyun.facade.actiontrail import ActiontrailFacade
from ScoutSuite.providers.ksyun.authentication_strategy import KsyunCredentials


class KsyunFacade:
    def __init__(self, credentials: KsyunCredentials):
        self._credentials = credentials
        self._instantiate_facades()

    def _instantiate_facades(self):
        self.actiontrail = ActiontrailFacade(self._credentials)
        self.kec = KECFacade(self._credentials)
        self.ram = RAMFacade(self._credentials)

    async def build_region_list(self, service: str, chosen_regions=None):

        # TODO could need this for service ids
        # service = 'ec2containerservice' if service == 'kec' else service

        # TODO does a similar endpoint exist?
        # available_services = await run_concurrently(lambda: Session().get_available_services())
        # if service not in available_services:
        #     raise Exception('Service ' + service + ' is not available.')

        headers = {
            'Host': 'kec.console.ksyun.com',
            'X-Requested-With': 'XMLHttpRequest',
            'Cookie': 'kscdigest=77372c6d1d6114859e1b9179b846dcbf-2304583564;'
        }

        params = {
            'Action': 'RegionList',
            'Service': 'kec',
            'Version': '2016-03-04',
            'source': 'kec',
            'Region': 'cn-beijing-6',
        }
        try:
            regions = []
            response = requests.get('https://kec.console.ksyun.com/kecapi/', params=params, headers=headers, verify=False)
            if json.loads(response.text).get('data'):
                for item in json.loads(response.text).get('data'):
                    regions.append(item['regionCode'])
            if chosen_regions:
                return list((Counter(regions) & Counter(chosen_regions)).elements())
            else:
                return regions
        except Exception as e:
            print(e)
            exit()
        
