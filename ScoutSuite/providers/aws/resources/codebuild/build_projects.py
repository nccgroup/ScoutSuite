from ScoutSuite.providers.aws.facade.base import AWSFacade
from ScoutSuite.providers.aws.resources.base import AWSResources
from ScoutSuite.providers.utils import get_non_provider_id


class BuildProjects(AWSResources):
    def __init__(self, facade: AWSFacade, region: str):
        super().__init__(facade)
        self.region = region

    async def fetch_all(self):
        raw_projects = await self.facade.codebuild.get_projects(self.region)
        for list_raw_project in raw_projects:
            for raw_project in list_raw_project.get('projects'):
                id, build_project = self._parse_build_projects(raw_project)
                self[id] = build_project

    def _parse_build_projects(self, raw_build_project):
        project_dict = {}
        project_dict['id'] = raw_build_project.get('arn')
        project_dict['arn'] = raw_build_project.get('arn')
        project_dict['name'] = raw_build_project.get('name')
        if 'vpcConfig' in raw_build_project:
            project_dict['vpc'] = raw_build_project.get('vpcConfig').get('vpcId')
            project_dict['subnets'] = raw_build_project.get('vpcConfig').get('subnets')
            project_dict['security_groups'] = raw_build_project.get('vpcConfig').get('securityGroupIds')
        return project_dict['id'], project_dict
