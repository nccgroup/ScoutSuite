from ScoutSuite.providers.gcp.resources.projects import Projects
from ScoutSuite.providers.gcp.resources.cloudsql.database_instances import DatabaseInstances
from ScoutSuite.providers.gcp.resources.cloudsql.postgresql_instances import PostgreSQLDatabaseInstances


class CloudSQL(Projects):
    _children = [ 
        (DatabaseInstances, 'instances'),
        (PostgreSQLDatabaseInstances, 'postgresql_instances')
     ]
