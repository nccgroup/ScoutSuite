from ScoutSuite.providers.aws.facade.utils import AWSFacadeUtils
from ScoutSuite.providers.aws.aws import handle_truncated_response
from ScoutSuite.providers.utils import run_concurrently


class EFSFacade:
    async def get_file_systems(self, region: str):
        file_systems = await AWSFacadeUtils.get_all_pages('efs', region, 'describe_file_systems', 'FileSystems')

        client = AWSFacadeUtils.get_client('efs', region)
        for file_system in file_systems:
            file_system_id = file_system['FileSystemId']
            file_system['Tags'] = await run_concurrently(
                        lambda: client.describe_tags(FileSystemId=file_system_id)['Tags']
            )

            # Get mount targets
            mount_targets = await AWSFacadeUtils.get_all_pages('efs', region, 'describe_mount_targets', 'MountTargets', FileSystemId=file_system_id)
            file_system['MountTargets'] = {}
            for mt in mount_targets:
                mount_target_id = mt['MountTargetId']
                file_system['MountTargets'][mount_target_id] = mt

                # Get security groups
                security_groups = run_concurrently(
                            lambda: client.describe_mount_target_security_groups(MountTargetId=mount_target_id)['SecurityGroups']
                )
                file_system['MountTargets'][mount_target_id]['SecurityGroups'] = security_groups

        return file_systems
