import React from 'react';
import PropTypes from 'prop-types';
import get from 'lodash/get';

import { Partial, PartialSection, PartialValue } from '../../../components/Partial';
import {
  partialDataShape,
  convertBoolToEnable,
  convertListToChips,
} from '../../../utils/Partials';
import { TabsMenu, TabPane } from '../../../components/Tabs';
import { renderList, valueOrNone } from '../../../utils/Partials/index';
import InformationsWrapper from '../../../components/InformationsWrapper';

const renderCIRBlock = ({ displayName, cidrBlock }) =>
  `${displayName}: ${cidrBlock}`;

const renderNodePools = nodePools => {
  return Object.entries(nodePools).map(([key]) => (
    <div key={key}>

      <h3>{key}</h3>
      <PartialSection path={key}>
        <PartialValue
          label="Automatic node upgrades"
          valuePath="auto_upgrade_enabled"
          renderValue={convertBoolToEnable}
        />

        <PartialValue
          label="Automatic node repair"
          valuePath="auto_repair_enabled"
          renderValue={convertBoolToEnable}
        />

        <PartialValue
          label="Legacy metadata endpoints"
          valuePath="legacy_metadata_endpoints_enabled"
          renderValue={convertBoolToEnable}
        />
      </PartialSection>

      
    </div>
  ));
};

const propTypes = {
  data: PropTypes.shape(partialDataShape).isRequired,
};

const K8SClusters = props => {
  const { data } = props;
  const item = get(data, ['item'], {});

  if (!data) return null;

  return (
    <Partial data={data}>
      <InformationsWrapper>
        <PartialValue
          label="Name"
          valuePath="name" />

        <PartialValue
          label="Project ID"
          valuePath="project" />

        <PartialValue
          label="Dashboard"
          valuePath="dashboard_status" />

        <PartialValue
          label="Alias IP"
          valuePath="alias_ip_enabled"
          renderValue={convertBoolToEnable}
        />

        <PartialValue
          label="Basic Authentication"
          valuePath="basic_authentication_enabled"
          renderValue={convertBoolToEnable}
        />

        <PartialValue
          label="Client Certificate Authentication"
          valuePath="client_certificate_enabled"
          renderValue={convertBoolToEnable}
        />

        <PartialValue
          label="Image Type"
          valuePath="image_type"
          errorPath="container_optimized_os_not_used" />

        <PartialValue
          label="Legacy Authorization"
          valuePath="legacy_abac_enabled"
          renderValue={convertBoolToEnable}
        />

        <PartialValue
          label="Master Authorized Networks"
          valuePath="master_authorized_networks_enabled"
          errorPath="master_authorized_networks_disabled"
          renderValue={convertBoolToEnable}
        />

        <PartialValue
          label="Pod Security Policy"
          valuePath="pod_security_policy_enabled"
          renderValue={convertBoolToEnable}
        />

        <PartialValue
          label="Network Policy"
          valuePath="network_policy_enabled"
          errorPath="network_policy_disabled"
          renderValue={convertBoolToEnable}
        />

        <PartialValue
          label="Private Cluster"
          valuePath="private_cluster_enabled"
          errorPath="private_cluster_disabled"
          renderValue={convertBoolToEnable}
        />

        <PartialValue
          label="Private Google Access"
          valuePath="private_ip_google_access_enabled"
          errorPath="private_ip_google_access_disabled"
          renderValue={convertBoolToEnable}
        />

        <PartialValue
          label="Service Account"
          valuePath="service_account"
          errorPath="default_service_account_used" />

        <PartialValue
          label="Stackdriver Logging"
          valuePath="logging_enabled"
          errorPath="logging_disabled"
          renderValue={convertBoolToEnable}
        />

        <PartialValue
          label="Stackdriver Monitoring"
          valuePath="monitoring_enabled"
          errorPath="monitoring_disabled"
          renderValue={convertBoolToEnable}
        />

        <PartialValue
          label="Scopes"
          valuePath="scopes"
          errorPath="scopes_not_limited"
          renderValue={values => renderList(values, '', valueOrNone)}
        />

        {item.labels && (
          <PartialValue
            label="Labels"
            valuePath="labels"
            errorPath="has_no_labels"
            renderValue={convertListToChips}
          />
        )}
      </InformationsWrapper>

      <TabsMenu>
        <TabPane title="Master Authorized Networks">
          <PartialValue
            label="Status"
            valuePath="master_authorized_networks_config.enabled"
            renderValue={convertBoolToEnable}
          />

          <PartialValue
            label="CIDR Blocks"
            valuePath="master_authorized_networks_config.cidrBlocks"
            renderValue={values => renderList(values, '', renderCIRBlock)}
          />
        </TabPane>

        <TabPane title="Node pools">{renderNodePools(item.node_pools)}</TabPane>
      </TabsMenu>
    </Partial>
  );
};

K8SClusters.propTypes = propTypes;

export default K8SClusters;
