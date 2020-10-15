from ScoutSuite.providers.aws.facade.base import AWSFacade
from ScoutSuite.providers.aws.resources.base import AWSResources
from ScoutSuite.providers.utils import get_non_provider_id


class Distributions(AWSResources):
    async def fetch_all(self):
        list_distributions = await self.facade.cloudfront.get_distributions()
        for distribution in list_distributions:
            id, distro = self._parse_distributions(distribution)
            self[id] = distro

    def _parse_distributions(self, distribution):
        distribution_dict = {}
        distribution_dict['id'] = distribution.get('Id')
        distribution_dict['arn'] = distribution.get('ARN')
        distribution_dict['status'] = distribution.get('Status')
        distribution_dict['last_modified_time'] = distribution.get('LastModifiedTime')
        distribution_dict['aliases'] = distribution.get('Aliases')
        distribution_dict['domain_name'] = distribution.get('DomainName')
        distribution_dict['origins'] = distribution.get('Origins')
        distribution_dict['viewer_protocol_policy'] = distribution.get('ViewerProtocolPolicy')
        distribution_dict['allowed_methods'] = distribution.get('AllowedMethods')
        distribution_dict['view_certificate'] = distribution.get('ViewerCertificate')
        distribution_dict['restrictions'] = distribution.get('Restrictions')
        distribution_dict['alias_icp_recordals'] = distribution.get('AliasICPRecordals')
        return distribution_dict['id'], distribution_dict
