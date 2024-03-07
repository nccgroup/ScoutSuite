from ScoutSuite.providers.aws.facade.base import AWSFacade
from ScoutSuite.providers.aws.resources.base import AWSResources
from ScoutSuite.providers.utils import get_non_provider_id


class Repositories(AWSResources):
    def __init__(self, facade: AWSFacade, region: str):
        super().__init__(facade)
        self.region = region

    async def fetch_all(self):
        raw_repositories = await self.facade.ecr.get_repositories(self.region)
        for raw_repository in raw_repositories:
            name, resource = self._parse_repository(raw_repository)
            self[name] = resource

    def _parse_repository(self, raw_repository):
        repo = {}
        repo['name'] = raw_repository['repositoryName']
        repo['id'] = raw_repository['registryId']
        repo['arn'] = raw_repository['repositoryArn']
        repo['created_at'] = raw_repository['createdAt'].strftime('%Y-%m-%d %H:%M:%S')
        repo['imageTagMutability'] = raw_repository['imageTagMutability']
        repo['Scan_on_Push'] = raw_repository['imageScanningConfiguration']['scanOnPush']
        repo['encryptionType'] = raw_repository['encryptionConfiguration']['encryptionType']
        repo['region'] = self.region
        
        return get_non_provider_id(repo['name']), repo