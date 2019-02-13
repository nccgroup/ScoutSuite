# -*- coding: utf-8 -*-

from ScoutSuite.providers.azure.configs.base import AzureBaseConfig


class SecurityCenterConfig(AzureBaseConfig):
    targets = (
        ('pricings', 'Pricings', 'list', {}, False),
        ('security_contacts', 'Security Contacts', 'list', {}, False),
        ('auto_provisioning_settings', 'Auto Provisioning Settings', 'list', {}, False)
    )

    def __init__(self, thread_config):
        self.pricings = {}
        self.pricings_count = 0

        self.security_contacts = {}
        self.security_contacts_count = 0

        self.auto_provisioning_settings = {}
        self.auto_provisioning_settings_count = 0

        super(SecurityCenterConfig, self).__init__(thread_config)

    def parse_pricings(self, pricing, params):
        pricing_dict = {}
        pricing_dict['id'] = pricing.id
        pricing_dict['name'] = pricing.name
        pricing_dict['pricing_tier'] = pricing.pricing_tier

        self.pricings[pricing_dict['id']] = pricing_dict

    def parse_security_contacts(self, security_contact, params):
        security_contact_dict = {}
        security_contact_dict['id'] = security_contact.id
        security_contact_dict['name'] = security_contact.name
        security_contact_dict['email'] = security_contact.email
        security_contact_dict['phone'] = security_contact.phone
        security_contact_dict['alert_notifications'] = security_contact.alert_notifications == "On"
        security_contact_dict['alerts_to_admins'] = security_contact.alerts_to_admins == "On"
        security_contact_dict['additional_properties'] = security_contact.additional_properties

        self.security_contacts[security_contact_dict['id']] = security_contact_dict

    def parse_auto_provisioning_settings(self, auto_provisioning_setting, params):
        auto_provisioning_setting_dict = {}
        auto_provisioning_setting_dict['id'] = auto_provisioning_setting.id
        auto_provisioning_setting_dict['name'] = auto_provisioning_setting.name
        auto_provisioning_setting_dict['auto_provision'] = auto_provisioning_setting.auto_provision

        self.auto_provisioning_settings[auto_provisioning_setting_dict['id']] = auto_provisioning_setting_dict
