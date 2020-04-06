from ScoutSuite.providers.aws.resources.base import AWSResources
from ScoutSuite.providers.utils import get_non_provider_id


class CredentialReports(AWSResources):
    async def fetch_all(self):
        raw_credential_reports = await self.facade.iam.get_credential_reports()
        for raw_credential_report in raw_credential_reports:
            name, resource = self._parse_credential_reports(raw_credential_report)
            self[name] = resource

    def _parse_credential_reports(self, raw_credential_report):
        user_id = raw_credential_report['user']
        raw_credential_report['name'] = user_id
        raw_credential_report['id'] = user_id
        raw_credential_report['password_last_used'] = self._sanitize_date(raw_credential_report['password_last_used'])
        raw_credential_report['access_key_1_last_used_date'] =\
            self._sanitize_date(raw_credential_report['access_key_1_last_used_date'])
        raw_credential_report['access_key_2_last_used_date'] =\
            self._sanitize_date(raw_credential_report['access_key_2_last_used_date'])
        raw_credential_report['last_used'] = self._compute_last_used(raw_credential_report)
        return get_non_provider_id(user_id), raw_credential_report

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
