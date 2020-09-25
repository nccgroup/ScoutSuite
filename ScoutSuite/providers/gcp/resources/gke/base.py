from ScoutSuite.providers.gcp.resources.gke.zones import GKEZones
from ScoutSuite.providers.gcp.resources.projects import Projects


class KubernetesEngine(Projects):
    _children = [
        (GKEZones, 'zones'),
    ]

    async def fetch_all(self):
        await Projects.fetch_all(self)
        # Clusters are resources with 2 levels of filtering 
        # (project and zone), so we need to propagate their count up.
        # Normally this would be done by setting the resource counts in the 
        # Zone class, but having a "zones_count" field in its 
        # dictionary causes errors in the rule engine.
        self['clusters_count'] = sum(sum(
            zone['clusters_count'] for zone in project['zones'].values()) for project in self['projects'].values())
        del self['zones_count']
