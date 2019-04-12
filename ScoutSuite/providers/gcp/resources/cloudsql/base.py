from ScoutSuite.providers.gcp.facade.gcp import GCPFacade
from ScoutSuite.providers.gcp.resources.projects import Projects
from ScoutSuite.providers.gcp.resources.cloudsql.database_instances import DatabaseInstances

class CloudSQL(Projects):
    _children = [ 
        (DatabaseInstances, 'instances')
     ]

    def __init__(self, gcp_facade: GCPFacade):
        super(CloudSQL, self).__init__(gcp_facade)
        