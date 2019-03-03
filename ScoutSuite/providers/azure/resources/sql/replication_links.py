# -*- coding: utf-8 -*-

from ScoutSuite.providers.base.configs.resources import Resources


class ReplicationLinks(Resources):

    def __init__(self, resource_group_name, server_name, database_name, facade):
        self.resource_group_name = resource_group_name
        self.server_name = server_name
        self.database_name = database_name
        self.facade = facade

    # TODO: make it really async.
    async def fetch_all(self):
        links = list(self.facade.replication_links.list_by_database(
            self.resource_group_name, self.server_name, self.database_name))
        self._parse_links(links)

    def _parse_links(self, links):
        self.update({
            'replication_configured': len(links) > 0
        })
