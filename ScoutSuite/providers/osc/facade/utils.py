from osc_sdk_python import Gateway


class OSCFacadeUtils:
    @staticmethod
    async def get_all_security_groups(session: Gateway):
        response = session.ReadSecurityGroups()
        security_groups = []
        if 'SecurityGroups' in response:
            for security_group in response['SecurityGroups']:
                security_groups.append(security_group)
        return security_groups

    @staticmethod
    async def get_all_volumes(session: Gateway):
        response = session.ReadVolumes()
        volumes = []
        if 'Volumes' in response:
            for volume in response['Volumes']:
                volumes.append(volume)
        return volumes

    @staticmethod
    async def get_all_snapshots(session: Gateway):
        response = session.ReadSnapshots()
        snapshots = []
        if 'Snapshots' in response:
            for snapshot in response['Snapshots']:
                snapshots.append(snapshot)
        return snapshots


    @staticmethod
    def _get_outscale_endpoint(region, version, action):
        return "https://api.{}.outscale.com/api/{}/{}".format(
            region,
            version,
            action
        )
