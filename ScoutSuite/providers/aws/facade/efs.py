from ScoutSuite.providers.aws.facade.utils import AWSFacadeUtils
from ScoutSuite.providers.utils import run_concurrently
from ScoutSuite.providers.aws.facade.basefacade import AWSBaseFacade


class EFSFacade(AWSBaseFacade):
    async def get_file_systems(self, region: str):
        file_systems = await AWSFacadeUtils.get_all_pages(
            'efs', region, self.session, 'describe_file_systems', 'FileSystems')
        await AWSFacadeUtils.get_and_set_concurrently(
            [self._get_and_set_tags, self._get_and_set_mount_targets], file_systems, region=region)

        return file_systems

    async def _get_and_set_tags(self, file_system: {}, region: str):
        client = AWSFacadeUtils.get_client('efs', self.session, region)
        file_system['Tags'] = await run_concurrently(
            lambda: client.describe_tags(FileSystemId=file_system['FileSystemId'])['Tags'])

    async def _get_and_set_mount_targets(self, file_system: {}, region: str):
        file_system['MountTargets'] = {}
        mount_targets = await AWSFacadeUtils.get_all_pages(
            'efs', region, self.session, 'describe_mount_targets', 'MountTargets',
            FileSystemId=file_system['FileSystemId'])

        if len(mount_targets) == 0:
            return

        for mount_target in mount_targets:
            mount_target_id = mount_target['MountTargetId']
            file_system['MountTargets'][mount_target_id] = mount_target

        await AWSFacadeUtils.get_and_set_concurrently(
            [self._get_and_set_mount_target_security_groups], mount_targets, region=region)

    async def _get_and_set_mount_target_security_groups(self, mount_target: {}, region: str):
        client = AWSFacadeUtils.get_client('efs', self.session, region)
        mount_target['SecurityGroups'] = run_concurrently(lambda: client.describe_mount_target_security_groups(
                MountTargetId=mount_target['MountTargetId'])['SecurityGroups'])
