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
} from '../../../utils/Partials';
import { TabsMenu, TabPane } from '../../../components/Partial/PartialTabs';

const renderDatabases = (dbs, serverKey) => {
  if (!dbs || !dbs.length) return <span>None</span>;

  return dbs.map(([key, db]) => {
    const baseErrorPath = `sqldatabase.servers.${serverKey}.databases.${key}`;

    return (
      <PartialSection path={`databases.${key}`} key={db.id}>
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
          label="Threat detection"
          valuePath="threat_detection.threat_detection_enabled"
          errorPath="server_threat_detection_disabled"
          renderValue={convertBoolToEnable}
        />

        <PartialValue
          label="Threat detection alerts"
          valuePath="threat_detection.send_alerts_enabled"
          errorPath="server_send_threat_detection_alerts_disabled"
          renderValue={convertBoolToEnable}
        />

        <PartialValue
          label="Send threat detection alerts"
          valuePath="threat_detection.send_alerts_enabled"
          errorPath="server_send_threat_detection_alerts_disabled"
          renderValue={convertBoolToEnable}
        />

        <PartialValue
          label="Threat detection retention period"
          valuePath="retention_days"
          errorPath="server_low_threat_detection_retention"
        />

        <PartialValue
          label="Resource group"
          valuePath="resource_group_name"
          renderValue={valueOrNone}
        />
      </InformationsWrapper>

      <TabsMenu>
        <TabPane title="SQL Databases">
          {renderDatabases(Object.entries(item.databases), item.id)}
        </TabPane>
      </TabsMenu>
    </Partial>
  );
};

SQLServers.propTypes = propTypes;

export default SQLServers;
