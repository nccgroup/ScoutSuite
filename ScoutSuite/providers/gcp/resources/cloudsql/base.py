from ScoutSuite.providers.gcp.resources.projects import Projects
from ScoutSuite.providers.gcp.resources.cloudsql.database_instances import DatabaseInstances


class CloudSQL(Projects):
    _children = [ 
        (DatabaseInstances, 'instances')
    ]
