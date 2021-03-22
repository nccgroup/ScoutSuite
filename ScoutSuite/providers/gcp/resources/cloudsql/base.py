from ScoutSuite.providers.gcp.resources.projects import Projects
from ScoutSuite.providers.gcp.resources.cloudsql.database_instances import DatabaseInstances
from ScoutSuite.providers.gcp.resources.cloudsql.mysql_instances import MySQLDatabaseInstances


class CloudSQL(Projects):
    _children = [ 
        (DatabaseInstances, 'instances'),
        (MySQLDatabaseInstances, 'mysql_instances')
     ]
