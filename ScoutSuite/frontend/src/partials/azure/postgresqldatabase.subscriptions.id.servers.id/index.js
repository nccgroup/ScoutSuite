import React from 'react';
import PropTypes from 'prop-types';
import get from 'lodash/get';

import InformationsWrapper from '../../../components/InformationsWrapper';
import {
  Partial,
  PartialSection,
  PartialValue,
} from '../../../components/Partial';
import { partialDataShape } from '../../../utils/Partials';
import { TabsMenu, TabPane } from '../../../components/Partial/PartialTabs';


const propTypes = {
  data: PropTypes.shape(partialDataShape).isRequired,
};
const renderFirewallRules = (rules, serverKey) => {
  if (!rules || !rules.length) return <span>None</span>;

  return rules.map(([key, rule]) => {
    const baseErrorPath = `postgresqldatabase.servers.${serverKey}.postgresql_firewall_rules.${key}`;

    return (
      <PartialSection path={`postgresql_firewall_rules.${key}`} key={rule.id}>
        <li>
          <b>{key}</b>
          <PartialValue
            label="Firewall rule start IP"
            valuePath="start_ip"
            baseErrorPath={baseErrorPath}
          />

          <PartialValue
            label="Firewall rule end IP"
            valuePath="end_ip"
            baseErrorPath={baseErrorPath}
          />

        </li>
      </PartialSection>
    );
  });
};

const Servers = props => {

  const { data } = props;
  const item = get(data, ['item'], {});

  if (!data) return null;

  return (
    <Partial data={data}>
      <InformationsWrapper>
        <PartialValue
          label="PostgreSQL Server Name"
          valuePath="name" />
        <PartialValue
          label="Server SSL connection enforcement"
          valuePath="ssl_enforcement" />
        <PartialValue
          label="Log checkpoint server parameter"
          valuePath="name" />
        <PartialValue
          label="PostgreSQL Server Name"
          valuePath="log_checkpoints.value"
          errorPath="server_log_checkpoints_value" />
        <PartialValue
          label="Log connections server parameter"
          valuePath="log_connections.value"
          errorPath="server_log_connections_value" />
        <PartialValue
          label="Log disconnections server parameter"
          valuePath="log_disconnections.value"
          errorPath="server_log_disconnections_value" />
        <PartialValue
          label="Log duration server parameter"
          valuePath="log_duration.value"
          errorPath="server_log_duration_value" />
        <PartialValue
          label="Connection throttling server parameter"
          valuePath="connection_throttling.value"
          errorPath="server_connection_throttling_value" />
        <PartialValue
          label="Log retention days server parameter"
          valuePath="log_retention_days.value"
          errorPath="server_log_retention_days_value" />


      </InformationsWrapper>
      <TabsMenu>
        <TabPane title="Firewall Rules">
          <ul>
            {renderFirewallRules(Object.entries(item.postgresql_firewall_rules), item.id)}
          </ul>
        </TabPane>
      </TabsMenu>
    </Partial>
  );
};

Servers.propTypes = propTypes;

export default Servers;
