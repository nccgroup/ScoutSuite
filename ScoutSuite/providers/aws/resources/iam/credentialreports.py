from ScoutSuite.providers.aws.resources.base import AWSResources
from ScoutSuite.providers.utils import get_non_provider_id


class CredentialReports(AWSResources):
    async def fetch_all(self):
        raw_credential_reports = await self.facade.iam.get_credential_reports()
        raw_user_mfa_devices = await self.facade.iam._get_and_set_user_mfa_devices()
        for raw_credential_report in raw_credential_reports:
            name, resource = self._parse_credential_reports(raw_credential_report)
            self[name] = resource

        for raw_user_mfa_device in raw_user_mfa_devices:
            name, resource = self._parse_user_mfa_devices(raw_user_mfa_device)
            self[name] = resource

    # Parse the "Virtual MFA Devices" API call for each user and get the MFA serial number and a boolean whether the
    # MFA is hardware based or not.
    '''
    def _parse_user_mfa_devices(self, raw_user_mfa_device):
        raw_user_mfa_device['serial'] = raw_user_mfa_device['SerialNumber']
        raw_user_mfa_device['is_hardware'] = 
    '''

    def _parse_credential_reports(self, raw_credential_report):
        raw_credential_report['id'] = get_non_provider_id(raw_credential_report['user'])
        raw_credential_report['name'] = raw_credential_report['user']
        raw_credential_report['password_enabled'] = raw_credential_report['password_enabled']
        raw_credential_report['password_last_used'] = self._sanitize_date(raw_credential_report['password_last_used'])
        raw_credential_report['password_last_changed'] =\
            self._sanitize_date(raw_credential_report['password_last_changed'])
        raw_credential_report['access_key_1_active'] = raw_credential_report['access_key_1_active']
        raw_credential_report['access_key_1_last_used_date'] =\
            self._sanitize_date(raw_credential_report['access_key_1_last_used_date'])
        raw_credential_report['access_key_1_last_rotated'] = \
            self._sanitize_date(raw_credential_report['access_key_1_last_rotated'])
        raw_credential_report['access_key_2_active'] = raw_credential_report['access_key_2_active']
        raw_credential_report['access_key_2_last_used_date'] =\
            self._sanitize_date(raw_credential_report['access_key_2_last_used_date'])
        raw_credential_report['access_key_2_last_rotated'] = \
            self._sanitize_date(raw_credential_report['access_key_2_last_rotated'])
        raw_credential_report['last_used'] = self._compute_last_used(raw_credential_report)
        raw_credential_report['cert_1_active'] = raw_credential_report['cert_1_active']
        raw_credential_report['cert_2_active'] = raw_credential_report['cert_2_active']
        return raw_credential_report['id'], raw_credential_report

    @staticmethod
    def _sanitize_date(date):
        """
        Returns the date if it is not equal to 'N/A' or 'no_information', else returns None
        """
        return date if date != 'no_information' and date != 'N/A' else None

    @staticmethod
    def _compute_last_used(credential_report):
        dates = [credential_report['password_last_used'],
                 credential_report['access_key_1_last_used_date'],
                 credential_report['access_key_2_last_used_date']]

        dates = [date for date in dates if date is not None]
        return max(dates) if len(dates) > 0 else None
