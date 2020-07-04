from ScoutSuite.providers.azure.resources.base import AzureResources


class Applications(AzureResources):
    async def fetch_all(self):
        for raw_application in await self.facade.aad.get_applications():
            id, application = await self._parse_application(raw_application)
            self[id] = application

    async def _parse_application(self, raw_application):
        application_dict = {}
        application_dict['id'] = raw_application.object_id
        application_dict['app_id'] = raw_application.app_id
        application_dict['name'] = raw_application.display_name
        application_dict['additional_properties'] = raw_application.additional_properties
        application_dict['deletion_timestamp'] = raw_application.deletion_timestamp
        application_dict['object_type'] = raw_application.object_type
        application_dict['allow_guests_sign_in'] = raw_application.allow_guests_sign_in
        application_dict['allow_passthrough_users'] = raw_application.allow_passthrough_users
        application_dict['app_logo_url'] = raw_application.app_logo_url
        application_dict['app_roles'] = raw_application.app_roles
        application_dict['app_permissions'] = raw_application.app_permissions
        application_dict['available_to_other_tenants'] = raw_application.available_to_other_tenants
        application_dict['error_url'] = raw_application.error_url
        application_dict['group_membership_claims'] = raw_application.group_membership_claims
        application_dict['homepage'] = raw_application.homepage
        application_dict['identifier_uris'] = raw_application.identifier_uris
        application_dict['informational_urls'] = raw_application.informational_urls
        application_dict['is_device_only_auth_supported'] = raw_application.is_device_only_auth_supported
        application_dict['key_credentials'] = raw_application.key_credentials
        application_dict['known_client_applications'] = raw_application.known_client_applications
        application_dict['logout_url'] = raw_application.logout_url
        application_dict['oauth2_allow_implicit_flow'] = raw_application.oauth2_allow_implicit_flow
        application_dict['oauth2_allow_url_path_matching'] = raw_application.oauth2_allow_url_path_matching
        application_dict['oauth2_permissions'] = raw_application.oauth2_permissions
        application_dict['oauth2_require_post_response'] = raw_application.oauth2_require_post_response
        application_dict['org_restrictions'] = raw_application.org_restrictions
        application_dict['optional_claims'] = raw_application.optional_claims
        application_dict['password_credentials'] = raw_application.password_credentials
        application_dict['pre_authorized_applications'] = raw_application.pre_authorized_applications
        application_dict['public_client'] = raw_application.public_client
        application_dict['publisher_domain'] = raw_application.publisher_domain
        application_dict['reply_urls'] = raw_application.reply_urls
        application_dict['required_resource_access'] = raw_application.required_resource_access
        application_dict['saml_metadata_url'] = raw_application.saml_metadata_url
        application_dict['sign_in_audience'] = raw_application.sign_in_audience
        application_dict['www_homepage'] = raw_application.www_homepage
        return application_dict['id'], application_dict
