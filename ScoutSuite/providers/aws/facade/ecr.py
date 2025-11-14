from typing import Dict
from ScoutSuite.core.console import print_exception
from ScoutSuite.providers.aws.facade.utils import AWSFacadeUtils
from ScoutSuite.providers.aws.facade.basefacade import AWSBaseFacade
from ScoutSuite.providers.utils import map_concurrently, run_concurrently

class ECRFacade(AWSBaseFacade):

    async def get_repositories(self,region: str):
        ecr_client = AWSFacadeUtils.get_client('ecr', self.session, region)
        try:
            raw_repositories = await run_concurrently(
                lambda: ecr_client.describe_repositories()) 
        except Exception as e:
            print(f'Failed to describe ECR repository : {e}')
            return []
        
        repository_names = [repo.get('repositoryName') for repo in raw_repositories.get('repositories',[])]
        if not repository_names:
            return []
        

        return await map_concurrently(
            self._get_repository, repository_names, region = region)
    

    async def _get_repository(self, repository_name: str, region: str) -> Dict:
        ecr_client = AWSFacadeUtils.get_client('ecr', self.session, region)
        try:
            raw_repository = await run_concurrently(
                lambda: ecr_client.describe_repositories(repositoryNames=[repository_name]))          
        except Exception as e:
            print(f'Failed to describe ECR repository {repository_name} : {e}')
            return {}
        
        return raw_repository.get('repositories',[])[0]
    

    async def get_images(self, region: str, repository_name: str):
        ecr_client = AWSFacadeUtils.get_client('ecr', self.session, region)
        try:
            # Missing await here - this is an async operation
            raw_images = await run_concurrently(
                lambda: ecr_client.list_images(repositoryName=repository_name))
        except Exception as e:
            print(f'Failed to list images in ECR repository {repository_name}: {e}')
            return []

        image_ids = raw_images.get('imageIds', [])
        if not image_ids:
            return []

        # Get detailed image information for this specific repository
        return await self._get_images_for_repository(repository_name, image_ids, region)

    async def _get_images_for_repository(self, repository_name: str, image_ids: list, region: str) -> list:
        """Get detailed image information for a specific repository"""
        ecr_client = AWSFacadeUtils.get_client('ecr', self.session, region)
        try:
            raw_images = await run_concurrently(
                lambda: ecr_client.describe_images(repositoryName=repository_name))

            image_details = raw_images.get('imageDetails', [])
            return image_details

        except Exception as e:
            print(f'Failed to describe ECR images in repository {repository_name}: {e}')
            return []


