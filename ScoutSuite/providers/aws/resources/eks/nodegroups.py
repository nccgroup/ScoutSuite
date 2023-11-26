from ScoutSuite.providers.aws.facade.base import AWSFacade
from ScoutSuite.providers.aws.resources.base import AWSResources
from ScoutSuite.providers.base.resources.base import CompositeResources
from ScoutSuite.providers.utils import get_non_provider_id

class Nodegroups(AWSResources):
    def __init__(self, facade: AWSFacade, region: str):
        super().__init__(facade)
        self.region = region
        self.cluster_name = None

    async def fetch_all(self):
        if not self.cluster_name:
            self.cluster_name = await self._get_cluster_name()
        if self.cluster_name:
            raw_nodes = await self.facade.eks.get_nodegroups(self.region, self.cluster_name)
            for raw_node in raw_nodes:
                name, resource = self._parse_nodegroups(raw_node)
                self[name] = resource


    async def _get_cluster_name(self):
        raw_clusters = await self.facade.eks.get_clusters(self.region)
        for cluster in raw_clusters:
            if cluster['cluster']['name']:
                return cluster['cluster']['name']

    def _parse_nodegroups(self, raw_node):
        node = {}
        node['name'] = raw_node['nodegroupName']
        node['nodegroupArn'] = raw_node['nodegroupArn']
        node['clusterName'] = raw_node['clusterName']
        node['Nodegroup_version'] = raw_node['version']
        node['MinSize'] = raw_node['scalingConfig']['minSize']
        node['MaxSize'] = raw_node['scalingConfig']['maxSize']
        node['desiredSize'] = raw_node['scalingConfig']['desiredSize']
        node['Node_sg'] = raw_node['resources']['remoteAccessSecurityGroup']
        node['created_at'] = raw_node['createdAt'].strftime('%Y-%m-%d %H:%M:%S')
        node['modified_at'] = raw_node['modifiedAt'].strftime('%Y-%m-%d %H:%M:%S')
        node['status'] = raw_node['status']
        node['capacityType'] = raw_node['capacityType']
        node['region'] = self.region
        node['instanceTypes'] = raw_node['instanceTypes'][0]
        node['amiType'] = raw_node['amiType']
        node['diskSize'] = raw_node['diskSize']
        node['nodeRole'] = raw_node['nodeRole']

        return get_non_provider_id(node['name']), node