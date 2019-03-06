from ScoutSuite.providers.aws.facade.utils import AWSFacadeUtils
from ScoutSuite.providers.aws.aws import handle_truncated_response


class EFSFacade:
    def get_file_systems(self, region: str):
        file_systems = AWSFacadeUtils.get_all_pages('efs', region, 'describe_file_systems', 'FileSystems')

        client = AWSFacadeUtils.get_client('efs', region)
        for file_system in file_systems:
            file_system_id = file_system['FileSystemId']
            file_system['Tags'] = client.describe_tags(FileSystemId=file_system_id)['Tags']

            # Get mount targets
            mount_targets = AWSFacadeUtils.get_all_pages('efs', region, 'describe_mount_targets', 'MountTargets', FileSystemId=file_system_id)
            file_system['MountTargets'] = {}
            for mt in mount_targets:
                mount_target_id = mt['MountTargetId']
                file_system['MountTargets'][mount_target_id] = mt

                # Get security groups
                security_groups = client.describe_mount_target_security_groups(MountTargetId=mount_target_id)['SecurityGroups']
                file_system['MountTargets'][mount_target_id]['SecurityGroups'] = security_groups

        return file_systems