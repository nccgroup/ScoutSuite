from ScoutSuite.providers.aws.facade.base import AWSFacade
from ScoutSuite.providers.aws.resources.base import AWSResources
from ScoutSuite.providers.utils import get_non_provider_id


class Distributions(AWSResources):
    async def fetch_all(self):
        list_distributions = await self.facade.cloudfront.get_distributions()
        for distribution in list_distributions:
            id, distro = self._parse_distributions(distribution)
            self[id] = distro

    def _parse_distributions(self, raw_distribution):
        distribution_dict = {}
        distribution_dict['id'] = distribution_dict['name'] = raw_distribution.get('Id')
        distribution_dict['arn'] = raw_distribution.get('ARN')
        distribution_dict['aliases'] = raw_distribution.get('Aliases')
        distribution_dict['status'] = raw_distribution.get('Status')
        distribution_dict['cache_behaviors'] = raw_distribution.get('CacheBehaviors')
        distribution_dict['restrictions'] = raw_distribution.get('Restrictions')
        distribution_dict['origins'] = raw_distribution.get('Origins')
        distribution_dict['domain_name'] = raw_distribution.get('DomainName')
        distribution_dict['web_acl_id'] = raw_distribution.get('WebACLId')
        distribution_dict['price_class'] = raw_distribution.get('PriceClass')
        distribution_dict['enabled'] = raw_distribution.get('Enabled')
        distribution_dict['default_cache_behavior'] = raw_distribution.get('DefaultCacheBehavior')
        distribution_dict['is_ipv6_enabled'] = raw_distribution.get('IsIPV6Enabled')
        distribution_dict['comment'] = raw_distribution.get('Comment')
        distribution_dict['http_version'] = raw_distribution.get('HttpVersion')
        distribution_dict['viewer_certificate'] = raw_distribution.get('ViewerCertificate')
        distribution_dict['custom_error_responses'] = raw_distribution.get('CustomErrorResponses')
        distribution_dict['last_modified_time'] = raw_distribution.get('LastModifiedTime')
        distribution_dict['origin_groups'] = raw_distribution.get('OriginGroups')
        return distribution_dict['id'], distribution_dict

