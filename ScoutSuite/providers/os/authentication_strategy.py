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
                     os_keywords_mode=None,
                     os_config_mode=None,
                     os_cloud_name=None,
                     os_config_path=None,
                     os_auth_url=None,
                     os_region_name=None,
                     os_project_name=None,
                     os_project_domain_name=None,
                     username=None,
                     os_user_domain_name='Default',
                     password=None, **kwargs):

        try:
            if os_config_mode:
                if os_config_path:
                    environ['OS_CLIENT_CONFIG_FILE'] = os_config_path
                session = openstack.connection.Connection(cloud=os_cloud_name)

            elif os_keywords_mode:
                session = openstack.connection.Connection(auth_url=os_auth_url,
                                                          region_name=os_region_name,
                                                          project_name=os_project_name,
                                                          project_domain_name=os_project_domain_name,
                                                          username=username,
                                                          user_domain_name=os_user_domain_name,
                                                          password=password)
            else:
                raise AuthenticationException('Insufficient credentials provided')

            return OpenstackCredentials(session)

        except Exception as e:
            raise AuthenticationException(e)
