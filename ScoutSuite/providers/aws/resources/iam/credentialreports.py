from ScoutSuite.providers.aws.resources.base import AWSResources
from ScoutSuite.providers.utils import get_non_provider_id
from ScoutSuite.core.console import print_exception


class CredentialReports(AWSResources):
    async def fetch_all(self):
        raw_credential_reports = await self.facade.iam.get_credential_reports()
        for raw_credential_report in raw_credential_reports:
            name, resource = await self._parse_credential_reports(raw_credential_report)
            self[name] = resource

    async def _parse_credential_reports(self, raw_credential_report):
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

        if raw_credential_report['mfa_active'] == 'true':
            raw_credential_report['mfa_active_hardware'] = await \
                self._user_has_hardware_mfa_devices(raw_credential_report['name'])
        else:
            raw_credential_report['mfa_active_hardware'] = False

        raw_credential_report['partition'] = self.facade.partition

        return raw_credential_report['id'], raw_credential_report

    async def _user_has_hardware_mfa_devices(self, username):
        """
        For a given user, returns whether a hardware MFA device is configured.

        For normal users, virtual devices have serial numbers starting with "arn", so it's easy to validate.

        For the root user, it's not possible to list all the devices, so instead we check all the virtual devices
        to confirm if one is for the root user. If this is not the case, we can infer a hardware device is configured
        (since we know MFA is active for the root user but cannot find a virtual device).
        """
        try:
            if username == '<root_account>':
                devices = await self.facade.iam.get_virtual_mfa_devices()
                for device in devices:
                    # If no EnableDate the device has been disabled
                    if device.get('EnableDate') and device['User']['Arn'][-5:] == ':root':
                        return False
                return True
            else:
                devices = await self.facade.iam.get_user_mfa_devices(username)
                if devices:
                    for device in devices:
                        if device['SerialNumber'][0:4] == 'arn:':
                            return False
                    return True
                else:
                    return False
        except Exception as e:
            print_exception(f'Failed to infer hardware MFA configuration for user {username}: {e}')

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
