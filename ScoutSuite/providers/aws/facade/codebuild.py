from ScoutSuite.core.console import print_exception
from ScoutSuite.providers.aws.facade.basefacade import AWSBaseFacade
from ScoutSuite.providers.aws.facade.utils import AWSFacadeUtils
from ScoutSuite.providers.utils import run_concurrently, map_concurrently


class CodeBuild(AWSBaseFacade):
    async def get_projects(self, region: str):
        codebuild_client = AWSFacadeUtils.get_client('codebuild', self.session, region)
        try:
            projects = await run_concurrently(lambda: codebuild_client.list_projects()['projects'])
        except Exception as e:
            print_exception(f'Failed to get CodeBuild projects: {e}')
            return []
        else:
            if not projects:
                return []
            return await map_concurrently(self._get_project_details, projects, region=region)
        
    async def _get_project_details(self, project: str, region: str):
        codebuild_client = AWSFacadeUtils.get_client('codebuild', self.session, region)
        try:
            project_details = await run_concurrently(lambda: codebuild_client.batch_get_projects(names=[project]))
        except Exception as e:
            print_exception(f'Failed to get CodeBuild project details: {e}')
            return {}
        else:
            project_details.pop('ResponseMetadata')
            project_details.pop('projectsNotFound')
            return project_details
