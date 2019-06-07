from ScoutSuite.providers.gcp.resources.projects import Projects
from ScoutSuite.providers.gcp.resources.kms.keyrings import KeyRings


class KMS(Projects):
    _children = [
        (KeyRings, 'keyrings')
    ]
