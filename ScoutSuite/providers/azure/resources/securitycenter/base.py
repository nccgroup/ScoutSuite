from ScoutSuite.providers.azure.resources.subscriptions import Subscriptions

from .auto_provisioning_settings import AutoProvisioningSettings
from .pricings import Pricings
from .alerts import Alerts
from .security_contacts import SecurityContacts
# from .information_protection_policies import InformationProtectionPolicies
# from .settings import Settings
from .compliance_results import ComplianceResults
from .regulatory_compliance_results import RegulatoryComplianceResults


class SecurityCenter(Subscriptions):
    _children = [
        (AutoProvisioningSettings, 'auto_provisioning_settings'),
        (Pricings, 'pricings'),
        # (Alerts, 'alerts'),  # FIXME this needs to be tested with alert results...
        (SecurityContacts, 'security_contacts'),
        # (InformationProtectionPolicies, 'information_protection_policies'),  # FIXME this isn't properly implemented
        # (Settings, 'settings')  # FIXME this isn't implemented
        (ComplianceResults, 'compliance_results'),
        (RegulatoryComplianceResults, 'regulatory_compliance_results')
    ]
