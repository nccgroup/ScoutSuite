from ScoutSuite.providers.azure.resources.base import AzureResources


class Applications(AzureResources):
    async def fetch_all(self):
        for raw_application in await self.facade.aad.get_applications():
            id, application = await self._parse_application(raw_application)
            self[id] = application

    async def _parse_application(self, raw_application):
        application_dict = {}
        application_dict['id'] = raw_application.get('id')
        application_dict['app_id'] = raw_application.get('appId')
        application_dict['name'] = raw_application.get('displayName')
        # application_dict['additional_properties'] = raw_application.additional_properties
        application_dict['deletion_timestamp'] = raw_application.get('deletedDateTime')
        application_dict['object_type'] = 'Application'
        # application_dict['allow_guests_sign_in'] = raw_application.allow_guests_sign_in
        # application_dict['allow_passthrough_users'] = raw_application.allow_passthrough_users
        # application_dict['app_logo_url'] = raw_application.app_logo_url
        application_dict['app_roles'] = raw_application.get('appRoles')
        # application_dict['app_permissions'] = raw_application.app_permissions
        # application_dict['available_to_other_tenants'] = raw_application.available_to_other_tenants
        # application_dict['error_url'] = raw_application.error_url
        application_dict['group_membership_claims'] = raw_application.get('groupMembershipClaims')
        # application_dict['homepage'] = raw_application.homepage
        application_dict['identifier_uris'] = raw_application.get('identifierUris')
        application_dict['informational_urls'] = raw_application.get('info')
        application_dict['is_device_only_auth_supported'] = raw_application.get('isDeviceOnlyAuthSupported')
        application_dict['key_credentials'] = raw_application.get('keyCredentials')
        application_dict['known_client_applications'] = raw_application['api'].get('knownClientApplications')
        application_dict['logout_url'] = raw_application['web'].get('logoutUrl')
        # application_dict['oauth2_allow_implicit_flow'] = raw_application.oauth2_allow_implicit_flow
        # application_dict['oauth2_allow_url_path_matching'] = raw_application.oauth2_allow_url_path_matching
        application_dict['oauth2_permissions'] = raw_application['api'].get('oauth2PermissionScopes')
        # application_dict['oauth2_require_post_response'] = raw_application.get('oauth2RequirePostResponse')
        # only in beta
        # application_dict['org_restrictions'] = raw_application.get('orgRestrictions') # only in beta
        application_dict['optional_claims'] = raw_application.get('optionalClaims')
        application_dict['password_credentials'] = raw_application.get('passwordCredentials')
        application_dict['pre_authorized_applications'] = raw_application['api'].get('preAuthorizedApplications')
        application_dict['public_client'] = raw_application.get('publicClient')
        application_dict['publisher_domain'] = raw_application.get('publisherDomain')
        # application_dict['reply_urls'] = raw_application.reply_urls
        application_dict['required_resource_access'] = raw_application.get('requiredResourceAccess')
        # application_dict['saml_metadata_url'] = raw_application.saml_metadata_url
        application_dict['sign_in_audience'] = raw_application.get('signInAudience')
        application_dict['www_homepage'] = raw_application['web'].get('homePageUrl')
        return application_dict['id'], application_dict
