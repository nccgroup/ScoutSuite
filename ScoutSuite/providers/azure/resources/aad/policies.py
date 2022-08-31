from ScoutSuite.providers.azure.resources.base import AzureResources


class Policies(AzureResources):
    async def fetch_all(self):
        raw_policy = await self.facade.aad.get_policies()
        id, policy = await self._parse_policy(raw_policy)
        self[id] = policy

    async def _parse_policy(self, raw_policy):
        policy_dict = {}
        policy_dict['id'] = raw_policy.get('id')
        policy_dict['name'] = raw_policy.get('displayName')
        policy_dict['allow_invites_from'] = raw_policy.get('allowInvitesFrom')
        policy_dict[
            'allowed_to_sign_up_email_based_subscription'] = raw_policy.get('allowedToSignUpEmailBasedSubscriptions')
        policy_dict['allowed_to_use_SSPR'] = raw_policy.get('allowedToUseSSPR')
        policy_dict['allow_email_verified_users_to_join_organization'
                    ] = raw_policy.get('allowEmailVerifiedUsersToJoinOrganization')
        policy_dict['allowed_to_create_apps'] = raw_policy.get('defaultUserRolePermissions', {}).get('allowedToCreateApps')
        policy_dict['allowed_to_create_security_groups'
                    ] = raw_policy.get('defaultUserRolePermissions', {}).get('allowedToCreateSecurityGroups')
        policy_dict[
            'allowed_to_read_other_users'] = raw_policy.get('defaultUserRolePermissions', {}).get('allowedToReadOtherUsers')

        return policy_dict['id'], policy_dict
