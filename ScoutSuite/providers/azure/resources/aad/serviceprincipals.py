from ScoutSuite.providers.azure.resources.base import AzureResources


class ServicePrincipals(AzureResources):
    async def fetch_all(self):
        for raw_service_principal in await self.facade.aad.get_service_principals():
            id, service_principal = await self._parse_service_principal(raw_service_principal)
            # exclude built-in service principals
            if service_principal['publisher_name'] != 'Microsoft Services':
                self[id] = service_principal

    async def _parse_service_principal(self, raw_service_principal):
        service_principal_dict = {}
        service_principal_dict['id'] = raw_service_principal.object_id
        service_principal_dict['name'] = raw_service_principal.display_name
        service_principal_dict['additional_properties'] = raw_service_principal.additional_properties
        service_principal_dict['deletion_timestamp'] = raw_service_principal.deletion_timestamp
        service_principal_dict['object_type'] = raw_service_principal.object_type
        service_principal_dict['account_enabled'] = raw_service_principal.account_enabled
        service_principal_dict['alternative_names'] = raw_service_principal.alternative_names
        service_principal_dict['app_name'] = raw_service_principal.app_display_name
        service_principal_dict['app_id'] = raw_service_principal.app_id
        service_principal_dict['app_owner_tenant_id'] = raw_service_principal.app_owner_tenant_id
        service_principal_dict['app_role_assignment_required'] = raw_service_principal.app_role_assignment_required
        service_principal_dict['app_roles'] = raw_service_principal.app_roles
        service_principal_dict['error_url'] = raw_service_principal.error_url
        service_principal_dict['homepage'] = raw_service_principal.homepage
        service_principal_dict['key_credentials'] = raw_service_principal.key_credentials
        service_principal_dict['logout_url'] = raw_service_principal.logout_url
        service_principal_dict['oauth2_permissions'] = raw_service_principal.oauth2_permissions
        service_principal_dict['password_credentials'] = raw_service_principal.password_credentials
        service_principal_dict[
            'preferred_token_signing_key_thumbprint'] = raw_service_principal.preferred_token_signing_key_thumbprint
        service_principal_dict['publisher_name'] = raw_service_principal.publisher_name
        service_principal_dict['reply_urls'] = raw_service_principal.reply_urls
        service_principal_dict['saml_metadata_url'] = raw_service_principal.saml_metadata_url
        service_principal_dict['service_principal_names'] = raw_service_principal.service_principal_names
        service_principal_dict['service_principal_type'] = raw_service_principal.service_principal_type
        service_principal_dict['tags'] = raw_service_principal.tags

        service_principal_dict['roles'] = []  # this will be filled in `finalize()`

        return service_principal_dict['id'], service_principal_dict

