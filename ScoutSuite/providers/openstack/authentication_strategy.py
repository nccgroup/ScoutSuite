import openstack
from os import environ
from ScoutSuite.providers.base.authentication_strategy import AuthenticationStrategy, AuthenticationException


class OpenstackCredentials:

    def __init__(self, session):
        self.session = session


class OpenstackAuthenticationStrategy(AuthenticationStrategy):
    """
    Implements authentication for the Openstack provider
    """

    def authenticate(self,
                     openstack_keywords_mode=None,
                     openstack_config_mode=None,
                     openstack_cloud_name=None,
                     openstack_config_path=None,
                     openstack_auth_url=None,
                     openstack_region_name=None,
                     openstack_project_name=None,
                     openstack_project_domain_name=None,
                     username=None,
                     openstack_user_domain_name='Default',
                     password=None, **kwargs):

        try:
            if openstack_config_mode:
                if openstack_config_path:
                    environ['OS_CLIENT_CONFIG_FILE'] = openstack_config_path
                session = openstack.connection.Connection(cloud=openstack_cloud_name)

            elif openstack_keywords_mode:
                session = openstack.connection.Connection(auth_url=openstack_auth_url,
                                                          region_name=openstack_region_name,
                                                          project_name=openstack_project_name,
                                                          project_domain_name=openstack_project_domain_name,
                                                          username=username,
                                                          user_domain_name=openstack_user_domain_name,
                                                          password=password)
            else:
                raise AuthenticationException('Insufficient credentials provided')

            return OpenstackCredentials(session)

        except Exception as e:
            raise AuthenticationException(e)
