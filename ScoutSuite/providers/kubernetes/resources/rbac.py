from ScoutSuite.providers.kubernetes.resources.base import KubernetesCompositeResources, KubernetesResourcesWithFacade


class ClusterRoles(KubernetesResourcesWithFacade):
    async def fetch_all(self):
        data = self.facade.extra.get_resources().get('cluster_role')
        self.save(data)

class ClusterRoleBindings(KubernetesResourcesWithFacade):
    async def fetch_all(self):
        data = self.facade.extra.get_resources().get('cluster_role_binding')
        self.save(data)

class Roles(KubernetesResourcesWithFacade):
    async def fetch_all(self):
        data = self.facade.extra.get_resources().get('role')
        self.save(data)

class RoleBindings(KubernetesResourcesWithFacade):
    async def fetch_all(self):
        data = self.facade.extra.get_resources().get('role_binding')
        self.save(data)

class RBAC(KubernetesCompositeResources):
    _children = [
        (ClusterRoles, 'cluster_role'),
        (ClusterRoleBindings, 'cluster_role_binding'),
        (Roles, 'role'),
        (RoleBindings, 'role_binding'),
    ]

    PERMISSIVE_BINDING_KEYWORDS = ['admin', 'secret', 'manage', 'root']
    DODGY_SUBJECTS = ['system:unauthenticated', 'system:authenticated', 'system:anonymous']
    DANGEROUS_GRANTS = [
        ('create', 'pods'),
        ('create', 'pods/exec'),
        ('get', 'secrets'),
        ('get', 'configmaps'),
        ('escalate', ''),
        ('impersonate', ''),
    ]

    KEY_PERMISSIVE_BINDINGS = 'permissive_bindings'
    KEY_DODGY_SUBJECTS = 'dodgy_subjects'
    KEY_DANGEROUS_GRANTS = 'dangerous_grants'

    async def finalize(self):
        self[self.KEY_PERMISSIVE_BINDINGS] = {}
        self[self.KEY_DODGY_SUBJECTS] = {}
        self[self.KEY_DANGEROUS_GRANTS] = {}

        for child_name in ['cluster_role_binding', 'role_binding']:
            for version in self[child_name]:
                resources = self[f'{child_name}_{version}']['resources']
                for binding_name in resources:
                    binding = resources[binding_name]
                    role_name: str = binding['metadata']['name']

                    # set permissive bindings for cluster roles and roles
                    for keyword in self.PERMISSIVE_BINDING_KEYWORDS:
                        if keyword.lower() in role_name.lower():
                            self[self.KEY_PERMISSIVE_BINDINGS][f'''{binding['kind']}/{role_name}'''] = binding

                    # set dodgy subjects
                    for subject in binding['data'].get('subjects') or []:
                        if subject['name'] in self.DODGY_SUBJECTS:
                            subject_namespace = f'''[{subject['namespace']}] ''' if subject.get('namespace') else ''
                            action = f'''{subject_namespace}{binding['version']}/{subject['kind']}/{subject['name']}'''
                            dodgy_subjects = self[self.KEY_DODGY_SUBJECTS].get(action, [])
                            dodgy_subjects.append(binding)
                            self[self.KEY_DODGY_SUBJECTS][action] = dodgy_subjects

        for dangerous_verb, dangerous_resource in self.DANGEROUS_GRANTS:
            action = f'{dangerous_verb} {dangerous_resource}' if dangerous_resource else dangerous_verb
            self[self.KEY_DANGEROUS_GRANTS][action] = []

            child_name = 'cluster_role'
            for version in self[child_name]:
                resources = self[f'{child_name}_{version}']['resources']
                for role_name in resources:
                    role = resources[role_name]

                    for rule in role['data'].get('rules') or []:

                        verb_is_dangerous = False
                        resource_is_dangerous = False

                        for verb in rule['verbs']:
                            if verb in ['*', dangerous_verb]:
                                verb_is_dangerous = True
                                break

                        for _resources in rule.get('resources') or []:
                            if _resources in ['*', dangerous_resource] or dangerous_resource == '':
                                dangerous_resource = _resources
                                resource_is_dangerous = True
                                break

                        if not (verb_is_dangerous and resource_is_dangerous):
                            continue

                        binding_child_name = 'cluster_role_binding'
                        for binding_version in self[binding_child_name]:
                            binding_resources = self[f'{binding_child_name}_{binding_version}']['resources']
                            for binding_name in binding_resources:
                                binding = binding_resources[binding_name]

                                if binding['data']['roleRef']['name'] != role_name.split('_')[-1]:
                                    continue

                                subjects = binding['data']['subjects'] or []
                                if len(subjects) == 0:
                                    continue

                                for subject in subjects:
                                    self[self.KEY_DANGEROUS_GRANTS][action].append({
                                        'kind': subject['kind'],
                                        'name': subject['name'],
                                        'verb': dangerous_verb,
                                        'resource': dangerous_resource or '-',
                                        'binding_kind': binding['data']['roleRef']['kind'],
                                        'binding_name': binding['metadata']['name'],
                                        'namespace': subject.get('namespace') or '-'
                                    })
