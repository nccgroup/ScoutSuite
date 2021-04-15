import React from 'react';
import PropTypes from 'prop-types';

import { Partial, PartialValue } from '../../../components/Partial';
import { partialDataShape } from '../../../utils/Partials';
import InformationsWrapper from '../../../components/InformationsWrapper';

const propTypes = {
  data: PropTypes.shape(partialDataShape).isRequired,
};

const LoggingMetrics = props => {
  const { data } = props;

  if (!data) return null;

  return (
    <Partial data={data}>
      <InformationsWrapper>
        <PartialValue
          label="Project Ownership Assignment/Changes Log Metric Filter Exist"
          valuePath="project_ownership_assignments" />

        <PartialValue
          label="Audit Configuration Changes Log Metric Filter Exist"
          valuePath="audit_config_change" />

        <PartialValue
          label="Custom Role Changes Log Metric Filter Exist"
          valuePath="custom_role_change" />

        <PartialValue
          label="VPC Network Firewall Rule Changes Log Metric Filter Exist"
          valuePath="vpc_network_firewall_rule_change" />

        <PartialValue
          label="VPC Network Route Changes Log Metric Filter Exist"
          valuePath="vpc_network_route_change" />

        <PartialValue
          label="VPC Network Changes Log Metric Filter Exist"
          valuePath="vpc_network_change" />

        <PartialValue
          label="Cloud Storage IAM Permission Changes Log Metric Filter Exist"
          valuePath="cloud_storage_iam_permission_change" />

        <PartialValue
          label="SQL Instance Configuration Changes Log Metric Filter Exist"
          valuePath="sql_instance_conf_change" />

      </InformationsWrapper>
    </Partial>
  );
};

LoggingMetrics.propTypes = propTypes;

export default LoggingMetrics;
