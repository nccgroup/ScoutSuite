from ScoutSuite.providers.aws.facade.base import AWSFacade
from ScoutSuite.providers.aws.resources.base import AWSResources
from ScoutSuite.providers.utils import get_non_provider_id


class Images(AWSResources):
    def __init__(self, facade: AWSFacade, region: str):
        super().__init__(facade)
        self.region = region

    async def fetch_all(self):
        raw_repos = await self.facade.ecr.get_repositories(self.region)
        for raw_repo in raw_repos:
            repository_name = raw_repo.get('repositoryName')
            if repository_name:
                images = await self.facade.ecr.get_images(self.region, repository_name)
                for image in images:
                    name, resource = self._parse_images(image)
                    self[name] = resource

    def _parse_images(self, raw_repo):
        image = {}
        image['name'] = raw_repo['repositoryName']
        image['registryId'] = raw_repo['registryId']
        image['imageDigest'] = raw_repo['imageDigest']
        
        image_scan_status = raw_repo.get('imageScanStatus', {})
        image['imageScanEnabled'] = "False" if image_scan_status.get('status') is None else "True"

        image['ScanStatusMessage'] = image_scan_status.get('description', 'Not Scanned')
        
        image_scan_summary = raw_repo.get('imageScanFindingsSummary', {}).get('findingSeverityCounts', {})
        image['HighSeverityCounts'] = image_scan_summary.get('HIGH', 0)
        image['MediumSeverityCounts'] = image_scan_summary.get('MEDIUM', 0)
        image['InformationalSeverityCounts'] = image_scan_summary.get('INFORMATIONAL', 0)
        image['LowSeverityCounts'] = image_scan_summary.get('LOW', 0)
        
        image_scan_summary_completed = raw_repo.get('imageScanFindingsSummary', {}).get('imageScanCompletedAt')
        image['imageScanFindingsSummaryCompleted'] = image_scan_summary_completed.strftime('%Y-%m-%d %H:%M:%S') if image_scan_summary_completed else ''
        
        return get_non_provider_id(image['imageDigest']), image