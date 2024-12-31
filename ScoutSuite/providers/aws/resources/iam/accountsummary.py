from ScoutSuite.providers.aws.resources.base import AWSResources

class AccountSummary(AWSResources):
    async def fetch_all(self):
        raw_account_summary = await self.facade.iam.get_account_summary()
        account_summary = self._parse_account_summary(raw_account_summary)
        self.update(account_summary)

    def _parse_account_summary(self, raw_account_summary):
        if raw_account_summary is None:
            return {
                'Users': 0,
                'Roles': 0,
                'Groups': 0,
                'Policies': 0,
                'InstanceProfiles': 0,
                'AccountAccessKeysPresent': 0,
                'AccountPasswordPresent': 0,
                'AccountMFAEnabled': 0,
                'MFADevicesInUse': 0,
                'MFADevices': 0,
                'AccountSigningCertificatesPresent': 0,
                'PolicyVersionsInUse': 0,
                'ServerCertificates': 0
            }

        return raw_account_summary
