from ScoutSuite.providers.base.resources.base import Resources
from ScoutSuite.providers.gcp.facade.base import GCPFacade


class LoggingMetrics(Resources):
    def __init__(self, facade: GCPFacade, project_id: str):
        super().__init__(facade)
        self.project_id = project_id

    async def fetch_all(self):
        raw_metrics = await self.facade.stackdriverlogging.get_metrics(self.project_id)
        metric = self._parse_metric(raw_metrics)
        self[self.project_id] = metric

    def _parse_metric(self, raw_metrics):
        metric_dict = {}
        metric_dict['project_ownership_assignments'] =\
            self._specific_filter_present(raw_metrics, '(protoPayload.serviceName="cloudresourcemanager.googleapis'
                                                       '.com") AND (ProjectOwnership OR projectOwnerInvitee) OR ('
                                                       'protoPayload.serviceData.policyDelta.bindingDeltas.action'
                                                       '="REMOVE" AND '
                                                       "protoPayload.serviceData.policyDelta.bindingDeltas.role"
                                                       '="roles/owner") OR ('
                                                       'protoPayload.serviceData.policyDelta.bindingDeltas.action'
                                                       '="ADD" AND '
                                                       'protoPayload.serviceData.policyDelta.bindingDeltas.role'
                                                       '="roles/owner")')
        metric_dict['audit_config_change'] = \
            self._specific_filter_present(raw_metrics, 'protoPayload.methodName="SetIamPolicy" AND '
                                                       'protoPayload.serviceData.policyDelta.auditConfigDeltas:*')
        metric_dict['custom_role_change'] = \
            self._specific_filter_present(raw_metrics, 'resource.type="iam_role" AND protoPayload.methodName =  '
                                                       '"google.iam.admin.v1.CreateRole" OR '
                                                       'protoPayload.methodName="google.iam.admin.v1.DeleteRole" OR '
                                                       'protoPayload.methodName="google.iam.admin.v1.UpdateRole"')
        metric_dict['vpc_network_firewall_rule_change'] = \
            self._specific_filter_present(raw_metrics, 'resource.type="gce_firewall_rule" AND '
                                                       'jsonPayload.event_subtype="compute.firewalls.patch" OR '
                                                       'jsonPayload.event_subtype="compute.firewalls.insert"')
        metric_dict['vpc_network_route_change'] = \
            self._specific_filter_present(raw_metrics, 'resource.type="gce_route" AND '
                                                       'jsonPayload.event_subtype="compute.routes.delete" OR '
                                                       'jsonPayload.event_subtype="compute.routes.insert"')
        metric_dict['vpc_network_change'] = \
            self._specific_filter_present(raw_metrics, 'resource.type=gce_network AND '
                                                       'jsonPayload.event_subtype="compute.networks.insert" OR '
                                                       'jsonPayload.event_subtype="compute.networks.patch" OR '
                                                       'jsonPayload.event_subtype="compute.networks.delete"  OR '
                                                       'jsonPayload.event_subtype="compute.networks.removePeering" OR '
                                                       'jsonPayload.event_subtype="compute.networks.addPeering"')
        metric_dict['cloud_storage_iam_permission_change'] = \
            self._specific_filter_present(raw_metrics, 'resource.type=gcs_bucket AND '
                                                       'protoPayload.methodName="storage.setIamPermissions"')
        metric_dict['sql_instance_conf_change'] = \
            self._specific_filter_present(raw_metrics, 'protoPayload.methodName="cloudsql.instances.update"')

        return metric_dict

    def _specific_filter_present(self, raw_metrics, filter_value: str):
        for metric in raw_metrics:
            if metric.filter_ == filter_value:
                return True
        return False
