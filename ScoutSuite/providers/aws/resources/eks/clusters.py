from ScoutSuite.providers.aws.facade.base import AWSFacade
from ScoutSuite.providers.aws.resources.base import AWSResources
from ScoutSuite.providers.utils import get_non_provider_id

class Clusters(AWSResources):
    def __init__(self, facade: AWSFacade, region: str):
        super().__init__(facade)
        self.region = region

    async def fetch_all(self):
        raw_clusters = await self.facade.eks.get_clusters(self.region)
        for raw_cluster in raw_clusters:
            name, resource = self._parse_cluster(raw_cluster)
            self[name] = resource

    def _parse_cluster(self, raw_cluster):
        cluster = {}
        cluster['name'] = raw_cluster['cluster']['name']
        cluster['status'] = raw_cluster['cluster']['status']
        cluster['arn'] = raw_cluster['cluster']['arn']
        cluster['created_at'] = raw_cluster['cluster']['createdAt'].strftime('%Y-%m-%d %H:%M:%S')
        cluster['endpoint'] = raw_cluster['cluster']['endpoint']
        cluster['role_arn'] = raw_cluster['cluster']['roleArn']
        cluster['version'] = raw_cluster['cluster']['version']
        cluster['endpointPublicAccess'] = raw_cluster['cluster']['resourcesVpcConfig']['endpointPublicAccess']
        cluster['endpointPrivateAccess'] = raw_cluster['cluster']['resourcesVpcConfig']['endpointPrivateAccess']
        cluster['cluster_sg_group'] = raw_cluster['cluster']['resourcesVpcConfig']['clusterSecurityGroupId']
        cluster['cluster_vpc'] = raw_cluster['cluster']['resourcesVpcConfig']['vpcId']
        cluster['logging'] = raw_cluster['cluster']['logging']['clusterLogging'][0]['enabled']
        cluster['region'] = self.region

        #extracting each logging type
        logging_types = raw_cluster['cluster']['logging']['clusterLogging']
        for log_type in logging_types:
            type_name = log_type['types'][0]
            type_enabled = log_type['enabled']
            cluster[f'type_logging_{type_name}'] = type_enabled
        
        return get_non_provider_id(cluster['name']), cluster