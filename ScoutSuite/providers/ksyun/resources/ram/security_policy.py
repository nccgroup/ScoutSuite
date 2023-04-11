from ScoutSuite.providers.ksyun.resources.base import KsyunResources
from ScoutSuite.providers.ksyun.facade.base import KsyunFacade


class SecurityPolicy(KsyunResources):
    def __init__(self, facade: KsyunFacade):
        super().__init__(facade)

    async def fetch_all(self):
        raw_security_policy = await self.facade.ram.get_security_policy()
        security_policy = self._parse_security_policy(raw_security_policy)
        self.update(security_policy)

    def _parse_security_policy(self, raw_security_policy):
        security_policy_dict = {
            'login_network_masks': raw_security_policy.get('mask_limit'),
            'login_session_duration': '6',
            'enable_save_mfa_ticket': raw_security_policy.get('bind_mode', {}).get('mfa'),
            'allow_user_change_password': True,
            'allow_user_manage_access_keys': False,
            'allow_user_manage_mfa_devices': False,
            'allow_user_manage_public_keys': False,
        }

        if security_policy_dict['login_network_masks'] == '':
            security_policy_dict['login_network_masks'] = None

        return security_policy_dict
