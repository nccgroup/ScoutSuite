from ScoutSuite.providers.aliyun.resources.base import AliyunResources
from ScoutSuite.providers.aliyun.facade.base import AliyunFacade


class SecurityPolicy(AliyunResources):
    def __init__(self, facade: AliyunFacade):
        super(SecurityPolicy, self).__init__(facade)

    async def fetch_all(self):
        raw_security_policy = await self.facade.ram.get_security_policy()
        security_policy = self._parse_security_policy(raw_security_policy)
        self.update(security_policy)

    def _parse_security_policy(self, raw_security_policy):
        security_policy_dict = {
            'login_network_masks':
                raw_security_policy.get('LoginProfilePreference', {}).get('LoginNetworkMasks'),
            'login_session_duration':
                raw_security_policy.get('LoginProfilePreference', {}).get('LoginSessionDuration'),
            'enable_save_mfa_ticket':
                raw_security_policy.get('LoginProfilePreference', {}).get('EnableSaveMFATicket'),
            'allow_user_change_password':
                raw_security_policy.get('LoginProfilePreference', {}).get('AllowUserToChangePassword'),
            'allow_user_manage_access_keys':
                raw_security_policy.get('AccessKeyPreference', {}).get('AllowUserToManageAccessKeys'),
            'allow_user_manage_mfa_devices':
                raw_security_policy.get('MFAPreference', {}).get('AllowUserToManageMFADevices'),
            'allow_user_manage_public_keys':
                raw_security_policy.get('PublicKeyPreference', {}).get('AllowUserToManagePublicKeys'),
        }

        if security_policy_dict['login_network_masks'] == '':
            security_policy_dict['login_network_masks'] = None

        return security_policy_dict
