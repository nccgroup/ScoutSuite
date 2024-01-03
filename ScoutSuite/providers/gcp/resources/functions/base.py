from ScoutSuite.providers.gcp.resources.functions.functions import Functions
from ScoutSuite.providers.gcp.resources.projects import Projects

class Functions(Projects):
    _children = [
        (Functions, 'functions')
    ]
