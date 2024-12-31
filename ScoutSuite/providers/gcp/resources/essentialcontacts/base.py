from ScoutSuite.providers.gcp.resources.essentialcontacts.contacts import Contacts
from ScoutSuite.providers.gcp.resources.projects import Projects

class EssentialContacts(Projects):
    _children = [(Contacts, 'contacts')]
