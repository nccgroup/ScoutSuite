from ScoutSuite.providers.aws.facade.utils import AWSFacadeUtils


class DirectConnectFacade:
    def get_connections(self, region):
        return AWSFacadeUtils.get_client('directconnect', region).describe_connections()['connections']