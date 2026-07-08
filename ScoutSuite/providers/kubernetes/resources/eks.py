from ScoutSuite.providers.kubernetes.resources.base import KubernetesCompositeResources, KubernetesResourcesWithFacade


class ControlPlaneLogging(KubernetesResourcesWithFacade):
    async def fetch_all(self):
        if not self.facade.eks:
            return

        cluster = self.facade.eks.get_cluster()

        '''
        Example output of `logging_configs`:
        [
            {'types': ['controllerManager', 'scheduler'], 'enabled': True},
            {'types': ['api', 'audit', 'authenticator'], 'enabled': False}
        ]
        '''
        logging_config = cluster['logging']['clusterLogging']
        for item in logging_config:
            for log_type in item['types']:
                item['name'] = log_type
                item['id'] = log_type
                self[log_type] = {
                    'name': log_type,
                    'id': log_type,
                    'enabled': item['enabled']
                }

class KMSEncryption(KubernetesResourcesWithFacade):
    async def fetch_all(self):
        if not self.facade.eks:
            return

        cluster = self.facade.eks.get_cluster()
        encryption_config = cluster.get('encryptionConfig') or []

        for item in encryption_config:
            arn = item['provider']['keyArn']
            item['name'] = arn
            item['id'] = arn
            self[arn] = item

class ResourcesVPCConfig(KubernetesResourcesWithFacade):
    async def fetch_all(self):
        if not self.facade.eks:
            return

        cluster = self.facade.eks.get_cluster()
        vpc_config = cluster['resourcesVpcConfig']

        self[vpc_config['vpcId']] = cluster['resourcesVpcConfig']
        self[vpc_config['vpcId']]['id'] = vpc_config['vpcId']
        self[vpc_config['vpcId']]['name'] = vpc_config['vpcId']

class EKS(KubernetesCompositeResources):
    _children = [
        (ControlPlaneLogging, 'logging'),
        (KMSEncryption, 'encryption'),
        (ResourcesVPCConfig, 'v_p_c'),
    ]
