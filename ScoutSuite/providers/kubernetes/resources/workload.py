from ScoutSuite.providers.kubernetes.resources.base import KubernetesCompositeResources, KubernetesResourcesWithFacade

class Pod(KubernetesResourcesWithFacade):
    async def fetch_all(self):
        data = self.facade.core.get_resources().get('pod')
        self.save(data)

class PodTemplate(KubernetesResourcesWithFacade):
    async def fetch_all(self):
        data = self.facade.core.get_resources().get('pod_template')
        self.save(data)

class CronJob(KubernetesResourcesWithFacade):
    async def fetch_all(self):
        data = self.facade.extra.get_resources().get('cron_job')
        self.save(data)

class DaemonSet(KubernetesResourcesWithFacade):
    async def fetch_all(self):
        data = self.facade.extra.get_resources().get('daemon_set')
        self.save(data)

class Deployment(KubernetesResourcesWithFacade):
    async def fetch_all(self):
        data = self.facade.extra.get_resources().get('deployment')
        self.save(data)

class Job(KubernetesResourcesWithFacade):
    async def fetch_all(self):
        data = self.facade.extra.get_resources().get('job')
        self.save(data)

class ReplicaSet(KubernetesResourcesWithFacade):
    async def fetch_all(self):
        data = self.facade.extra.get_resources().get('replica_set')
        self.save(data)

class StatefulSet(KubernetesResourcesWithFacade):
    async def fetch_all(self):
        data = self.facade.extra.get_resources().get('stateful_set')
        self.save(data)

class Workload(KubernetesCompositeResources):
    _children = [
        (Pod, 'pod'),
        (PodTemplate, 'pod_template'),
        (CronJob, 'cron_job'),
        (DaemonSet, 'daemon_set'),
        (Deployment, 'deployment'),
        (Job, 'job'),
        (ReplicaSet, 'replica_set'),
        (StatefulSet, 'stateful_set')
    ]

    container_path_prefixes = {
        'pod': ['data', 'spec'],
        'daemon_set': ['data', 'spec', 'template', 'spec'],
        'deployment': ['data', 'spec', 'template', 'spec'],
        'replica_set': ['data', 'spec', 'template', 'spec'],
        'pod_template': ['data', 'spec', 'template', 'spec'],
        'stateful_set': ['data', 'spec', 'template', 'spec'],
        'job': ['data', 'spec', 'template', 'spec'],
        'cron_job': ['data', 'spec', 'jobTemplate', 'spec', 'template', 'spec']
    }

    async def finalize(self):
        self['images'] = []

        for _, child_name in self._children:
            for version in self[child_name]:
                resources = self[f'{child_name}_{version}']['resources']
                for resource_name in resources:
                    spec = resources[resource_name]
                    for key in self.container_path_prefixes[child_name]:
                        spec = spec[key]

                    containers = spec['containers']
                    for container in containers:
                        self['images'].append(container['image'])

                    init_containers = spec.get('initContainers', [])
                    for container in init_containers:
                        self['images'].append(container['image'])

                    ephemeral_containers = spec.get('ephemeralContainers', [])
                    for container in ephemeral_containers:
                        self['images'].append(container['image'])

        self['images'] = list(set(self['images']))
        self['images'].sort()