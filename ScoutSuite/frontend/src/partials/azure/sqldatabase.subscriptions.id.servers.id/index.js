import React from 'react';
import PropTypes from 'prop-types';
import get from 'lodash/get';

import InformationsWrapper from '../../../components/InformationsWrapper';
import {
  Partial,
  PartialSection,
  PartialValue,
} from '../../../components/Partial';
import {
  convertBoolToEnable,
  partialDataShape,
  renderList,
  valueOrNone,
  convertListToChips
} from '../../../utils/Partials';
import { TabsMenu, TabPane } from '../../../components/Partial/PartialTabs';

const renderDatabases = (dbs, serverKey) => {
  if (!dbs || !dbs.length) return <span>None</span>;

  return dbs.map(([key, db]) => {
    const baseErrorPath = `sqldatabase.servers.${serverKey}.databases.${key}`;

    return (
      <PartialSection path={`databases.${key}`} key={db.id}>
        <li>

          <b>{key}</b>

          <PartialValue
            label="Auditing"
            valuePath="auditing.auditing_enabled"
            errorPath="db_auditing_disabled"
            renderValue={convertBoolToEnable}
            baseErrorPath={baseErrorPath}
          />

          <PartialValue
            label="Auditing retention period"
            valuePath="auditing.retention_days"
            errorPath="db_low_auditing_retention"
            baseErrorPath={baseErrorPath}
          />

          <PartialValue
            label="Threat detection"
            valuePath="threat_detection.threat_detection_enabled"
            errorPath="db_threat_detection_disabled"
            renderValue={convertBoolToEnable}
            baseErrorPath={baseErrorPath}
          />

          <PartialValue
            label="Threat detection alerts"
            valuePath="threat_detection.alerts_enabled"
            errorPath="db_threat_detection_alerts_disabled"
            renderValue={convertBoolToEnable}
            baseErrorPath={baseErrorPath}
          />

          <PartialValue
            label="Send threat detection alerts"
            valuePath="threat_detection.send_alerts_enabled"
            errorPath="db_send_threat_detection_alerts_disabled"
            renderValue={convertBoolToEnable}
            baseErrorPath={baseErrorPath}
          />

          <PartialValue
            label="Threat detection retention period"
            valuePath="threat_detection.retention_days"
            errorPath="db_low_threat_detection_retention"
            baseErrorPath={baseErrorPath}
          />

          <PartialValue
            label="Transparent data encryption"
            valuePath="transparent_data_encryption_enabled"
            errorPath="transparent_data_encryption_enabled"
            renderValue={convertBoolToEnable}
            baseErrorPath={baseErrorPath}
          />

          <PartialValue
            label="Geo-replication configured"
            valuePath="replication_configured"
            errorPath="replication_configured"
            renderValue={convertBoolToEnable}
            baseErrorPath={baseErrorPath}
          />

          <PartialValue
            label="Tags" valuePath="tags"
            renderValue={renderList} />

          <PartialValue
            label="Resource group"
            valuePath="resource_group_name"
            renderValue={valueOrNone}
            baseErrorPath={baseErrorPath}
          />
        </li>
      </PartialSection>
    );
  });
};
const renderFirewallRules = (rules, serverKey) => {
  if (!rules || !rules.length) return <span>None</span>;

  return rules.map(([key, rule]) => {
    const baseErrorPath = `sqldatabase.servers.${serverKey}.firewall_rules.${key}`;

    return (
      <PartialSection path={`firewall_rules.${key}`} key={rule.id}>
        <li>

          <b>{rule.name}</b>

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

const propTypes = {
  data: PropTypes.shape(partialDataShape).isRequired,
};

const SQLServers = props => {
  const { data } = props;
  const item = get(data, ['item'], {});

  if (!data) return null;

  return (
    <Partial data={data}>
      <InformationsWrapper>
        <PartialValue label="SQL Server Name" valuePath="name" />

        <PartialValue
          label="Azure Active Directory Admin"
          valuePath="ad_admin.login"
          errorPath="ad_admin"
          renderValue={valueOrNone}
        />

        <PartialValue
          label="Auditing"
          valuePath="auditing.auditing_enabled"
          errorPath="server_auditing_disabled"
          renderValue={convertBoolToEnable}
        />

        <PartialValue
          label="Auditing retention period"
          valuePath="auditing.retention_days"
          errorPath="server_low_auditing_retention"
        />

        <PartialValue
          label="Advanced Threat detection (ATP)"
          valuePath="threat_detection.threat_detection_enabled"
          errorPath="server_threat_detection_disabled"
          renderValue={convertBoolToEnable}
        />

        <PartialValue
          label="Advanced Threat Protection (ATP) alerts"
          valuePath="threat_detection.alerts_enabled"
          errorPath="server_threat_detection_alerts_disabled"
          renderValue={convertBoolToEnable}
        />

        <PartialValue
          label="Send Advanced Threat Protection (ATP) alerts"
          valuePath="threat_detection.send_alerts_enabled"
          errorPath="server_send_threat_detection_alerts_disabled"
          renderValue={convertBoolToEnable}
        />

        <PartialValue
          label="Advanced Threat Protection (ATP) retention period"
          valuePath="retention_days"
          errorPath="server_low_threat_detection_retention"
        />

        <PartialValue
          label="Storage account name"
          valuePath="server_vulnerability.storage_account_name"
          errorPath="server_vulnerability_storage_account_name"
          renderValue={valueOrNone}
        />
        <PartialValue
          label="Send email notification to admins and subscription owners"
          valuePath="server_vulnerability.email_subscription_admin"
          errorPath="server_vulnerability_email_subscription_admin"
          renderValue={convertBoolToEnable}
        />

        <PartialValue
          label="Periodic recurring scans"
          valuePath="server_vulnerability.recurring_scans_enabled"
          errorPath="server_vulnerability_recurring_scans_enabled"
          renderValue={convertBoolToEnable}
        />
        <PartialValue
          label="Send scan report to is configured"
          errorPath="server_vulnerability_send_scan_reports_to_not_empty"
          valuePath="server_vulnerability.send_scan_reports_to_not_empty"
          renderValue={valueOrNone}
        />
        <PartialValue
          label="TDE server key type"
          errorPath="server_encryption_protectors_TDE_protector_is_encrypted"
          valuePath="encryption_protectors.server_key_type"

        />
        <PartialValue
          label="Tags"
          valuePath="tags"
          renderValue={convertListToChips}
        />
      </InformationsWrapper>

      <TabsMenu>
        <TabPane title="SQL Databases">
          <ul>
            {renderDatabases(Object.entries(item.databases), item.id)}
          </ul>
        </TabPane>
        <TabPane title="Firewall Rules">
          <ul>
            {renderFirewallRules(Object.entries(item.firewall_rules), item.id)}
          </ul>
        </TabPane>
      </TabsMenu>
    </Partial>
  );
};



SQLServers.propTypes = propTypes;

export default SQLServers;
