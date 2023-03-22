
from ScoutSuite.providers.ksyun.resources.base import KsyunResources


class Trails(KsyunResources):
    async def fetch_all(self):
        for raw_trail in await self.facade.actiontrail.get_trails():
            id, trail = self._parse_trails(raw_trail)
            self[id] = trail

    def _parse_trails(self, raw_trail):
        trail_dict = {}
        trail_dict['id'] = raw_trail.get('EventId')
        trail_dict['region'] = raw_trail.get('Region')
        trail_dict['event_rw'] = raw_trail.get('EventRW')
        trail_dict['eventtype'] = raw_trail.get('EventType')
        trail_dict['eventname'] = raw_trail.get('EventName')
        trail_dict['eventsource'] = raw_trail.get('EventSource')
        trail_dict['servicename'] = raw_trail.get('ServiceName')
        trail_dict['usertype'] = raw_trail.get('UserIdentity').get('UserType')
        trail_dict['username'] = raw_trail.get('UserIdentity').get('UserName')
        trail_dict['accountid'] = raw_trail.get('UserIdentity').get('AccountId')

        return trail_dict['id'], trail_dict