import os
import re

from ScoutSuite.core.ruleset import Ruleset
from ScoutSuite.providers.base.provider import BaseProvider
from ScoutSuite.providers.kubernetes.authentication_strategy import ClusterProvider, KubernetesCredentials
from ScoutSuite.providers.kubernetes.resources.workload import Workload
from ScoutSuite.providers.kubernetes.services import KubernetesServicesConfig
from ScoutSuite.utils import formatted_service_name

class KubernetesProvider(BaseProvider):
    """
    Implements provider for Kubernetes
    """

    services_requiring_finding_deduplication = {
        'daemon_set': True,
        'deployment': True,
        'replica_set': True,
        'stateful_set': True,
        'pod': True,
    }

    composite_resources = {
        'loggingmonitoring': True,
        'eks': True,
        'kubernetesengine': True,
        'rbac': True,
        'version': True,
        'workload': True
    }

    def __init__(self, **kwargs):
        report_dir = kwargs.get('report_dir')
        timestamp = kwargs.get('timestamp')
        resources = kwargs.get('resources') or []
        skipped_resources = kwargs.get('skipped_resources') or []
        result_format = kwargs.get('result_format', 'json')

        self.credentials: KubernetesCredentials = kwargs.get('credentials')
        self.metadata_path = f'{os.path.split(os.path.abspath(__file__))[0]}/metadata.json'
        self.environment = 'kubernetes'
        self.provider_code = 'kubernetes'
        self.result_format = result_format
        self.services_config = KubernetesServicesConfig
        self.account_id = self.credentials.cluster_context
        self.provider_name = formatted_service_name.get(self.credentials.cluster_provider) or 'Kubernetes'

        self.original_containers = {
            'cron_job': [],
            'deployment': [],
            'job': [],
            'pod': [],
            'pod_template': [],
            'replica_set': [],
            'stateful_set': [],
        }

        super().__init__(report_dir, timestamp, resources, skipped_resources, result_format)

    def get_report_name(self):
        """
        Returns the name of the report using the provider's configuration
        """
        return f'''kubernetes-{self.credentials.cluster_context.replace(':', '-')}'''

    def preprocessing(self, ip_ranges=None, ip_ranges_name_key=None):
        provider = self.credentials.cluster_provider

        # delete cloud-specific services if necessary
        if provider != ClusterProvider.AKS.value:
            # TODO: have actual AKS findings
            if self.metadata.get(ClusterProvider.AKS.value[0]) and self.metadata[ClusterProvider.AKS.value[0]].get('loggingmonitoring'):
                del self.metadata[ClusterProvider.AKS.value[0]]['loggingmonitoring']
        if provider != ClusterProvider.EKS.value:
            if self.metadata.get(ClusterProvider.EKS.value[0]) and self.metadata[ClusterProvider.EKS.value[0]].get(ClusterProvider.EKS.value):
                del self.metadata[ClusterProvider.EKS.value[0]][ClusterProvider.EKS.value]
        if provider != ClusterProvider.GKE.value:
            if self.metadata.get(ClusterProvider.GKE.value[0]) and self.metadata[ClusterProvider.GKE.value[0]].get('kubernetesengine'):
                del self.metadata[ClusterProvider.GKE.value[0]]['kubernetesengine']

        # delete empty service groups
        service_groups_to_delete = []
        for service_group_name in self.metadata:
            if len(self.metadata[service_group_name]) == 0:
                service_groups_to_delete.append(service_group_name)

        for group_name in service_groups_to_delete:
            del self.metadata[group_name]

        for service_name in Workload.container_path_prefixes:
            keys = Workload.container_path_prefixes[service_name]
            service = self.services.get(service_name)
            if not service: continue
            versions = self._get_resource_versions(service)
            for version in versions:
                resources = service[version]['resources']
                for resource_id in resources:
                    spec = resources[resource_id]
                    for key in keys:
                        spec = spec[key]

                    containers = spec['containers']
                    self.original_containers[service_name] = list(containers)
                    init_containers = spec.get('initContainers', [])
                    ephemeral_containers = spec.get('ephemeralContainers', [])

                    containers.extend(init_containers)
                    containers.extend(ephemeral_containers)

        return super().preprocessing(ip_ranges, ip_ranges_name_key)

    def postprocessing(self, current_time, ruleset: Ruleset, run_parameters):
        self._postprocess_regular_resources()
        self._postprocess_composite_resource('workload')
        self._postprocess_composite_resource('rbac')
        
        for service_name in Workload.container_path_prefixes:
            keys = Workload.container_path_prefixes[service_name]
            service = self.services.get(service_name)
            if not service: continue
            versions = self._get_resource_versions(service)
            for version in versions:
                resources = service[version]['resources']
                for resource_id in resources:
                    spec = resources[resource_id]
                    for key in keys:
                        spec = spec[key]

                    spec['containers'] = self.original_containers[service_name]

        ## TODO: This needs to look better.
        # service_names = self._get_resource_versions(self.services['workload'])
        # for service_name in service_names:
        #     for finding_name in self.services[service_name]['findings']:
        #         self.services['workload']['findings'][finding_name] = self.services[service_name]['findings'][finding_name]

        return super().postprocessing(current_time, ruleset, run_parameters)

    def _get_resource_versions(self, service: dict):
        versions = filter(lambda key: service.get(f'{key}_count') != None, service)
        return list(versions)

    def _load_resource_metadata(self, service_group, service_name, versions):
        self.metadata[service_group] = self.metadata.get(service_group, {})
        self.metadata[service_group][service_name] = self.metadata[service_group].get(service_name, {})
        self.metadata[service_group][service_name]['resources'] = self.metadata[service_group][service_name].get('resources', {})
        self.metadata[service_group][service_name]['summaries'] = self.metadata[service_group][service_name].get('summaries', {})

        for version in versions:
            self.metadata[service_group][service_name]['resources'][version] = {
                'path': f'services.{service_name}.{version}'
            }

    def _postprocess_regular_resources(self):
        for service_name in self.services:
            service_group = service_name[0]
            service = self.services[service_name]

            if self.composite_resources.get(service_name): continue

            service_requires_finding_deduplication = self.services_requiring_finding_deduplication.get(service_name, False)

            versions = self._get_resource_versions(service)
            self._load_resource_metadata(service_group, service_name, versions)

            # post-process findings
            standalone_resources = {}
            standalone_resources_tampered = False

            for version in versions:
                # finding de-duplication
                if not service_requires_finding_deduplication: continue
                service_resources = self.services[service_name][version]['resources']
                for name in service_resources:
                    if not service_resources[name].get('ownerReferences'):
                        standalone_resources[f'''{service_name}.{version}.resources.{name}'''] = True
                        standalone_resources_tampered = True

            # remove resources that have owner references from findings
            findings = self.services[service_name]['findings']
            for finding_name in findings:
                finding = findings[finding_name]

                actual_finding_items = []
                for finding_item in finding['items']:
                    # e.g. pod.v1.resources.pod-name
                    if '.'.join(finding_item.split('.')[:4]) in standalone_resources:
                        actual_finding_items.append(finding_item)

                if standalone_resources_tampered:
                    finding['items'] = actual_finding_items
                    finding['checked_items'] = len(standalone_resources)
                    finding['flagged_items'] = min(finding['checked_items'], len(finding['items']))

                for version in versions:
                    items = finding['items']
                    for i in range(len(items)):
                        expression = f'^{service_name}\.{version}\.resources'
                        items[i] = re.sub(expression, f'{service_name}.{version}', items[i])

    def _postprocess_composite_resource(self, composite_resource_name):
        service_group  = '_scout_suite_aggregation'
        self.metadata[service_group] = self.metadata.get(service_group, {})

        service = self.services[composite_resource_name]
        versions = self._get_resource_versions(service)
        self._load_resource_metadata(service_group, composite_resource_name, versions)