from ScoutSuite.providers.base.resources.base import Resources
from ScoutSuite.providers.gcp.facade.base import GCPFacade
from ScoutSuite.core.console import print_exception


class Sinks(Resources):
    def __init__(self, facade: GCPFacade, project_id: str):
        super().__init__(facade)
        self.project_id = project_id

    async def fetch_all(self):
        raw_sinks = await self.facade.stackdriverlogging.get_sinks(self.project_id)
        parsing_error_counter = 0
        for raw_sink in raw_sinks:
            try:
                sink_name, sink = self._parse_sink(raw_sink)
                self[sink_name] = sink
            except Exception as e:
                parsing_error_counter += 1
        if parsing_error_counter > 0:
            print_exception(
                'Failed to parse {} resource: {} times'.format(self.__class__.__name__, parsing_error_counter))

    def _parse_sink(self, raw_sink):
        sink_dict = {}
        sink_dict['name'] = raw_sink.name
        sink_dict['filter'] = raw_sink.filter_
        sink_dict['destination'] = raw_sink.destination
        return sink_dict['name'], sink_dict
