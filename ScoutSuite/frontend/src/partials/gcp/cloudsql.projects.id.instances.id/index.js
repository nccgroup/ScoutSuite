import React from 'react';
import PropTypes from 'prop-types';
import get from 'lodash/get';

import { Partial, PartialValue } from '../../../components/Partial';
import {
  partialDataShape,
  convertBoolToEnable,
  formatDate,
  valueOrNone,
} from '../../../utils/Partials';
import { TabPane, TabsMenu } from '../../../components/Tabs';
import InformationsWrapper from '../../../components/InformationsWrapper';

const renderAuthorizedNetworks = items => {
  if (!items || items.length === 0) return <span>None</span>;

  return (
    <ul>
      {items.map((value, i) => {
        return (
          <li key={i}>
            <PartialValue
              errorPath={`authorized_networks.${i}.open_to_the_world`}
              value={value}
            />
          </li>
        );
      })}
    </ul>
  );
};

const propTypes = {
  data: PropTypes.shape(partialDataShape).isRequired,
};

const SQLInstances = props => {
  const { data } = props;
  const item = get(data, ['item'], {});

  if (!data) return null;

  return (
    <Partial data={data}>
      <InformationsWrapper>
        <PartialValue label="Project ID" valuePath="project_id" />

        <PartialValue
          label="Automatic Backups"
          valuePath="automatic_backup_enabled"
          renderValue={convertBoolToEnable}
        />

        <PartialValue
          label="Last Backup"
          valuePath="last_backup_timestamp"
          renderValue={formatDate}
        />

        <PartialValue
          label="Logs"
          valuePath="log_enabled"
          renderValue={convertBoolToEnable}
        />

        <PartialValue
          label="SSL Required"
          valuePath="ssl_required"
          renderValue={convertBoolToEnable}
        />

        <PartialValue
          label="Public IP Address"
          valuePath="public_ip"
          renderValue={valueOrNone}
        />

        <PartialValue
          label="Private IP Address"
          valuePath="private_ip"
          renderValue={valueOrNone}
        />

        <PartialValue
          label="Local Infile Flag is Off"
          valuePath="local_infile_off"
          renderValue={valueOrNone}
        />

        <PartialValue
          label="Cross db Ownership Chaining Flag is Off"
          valuePath="cross_db_ownership_chaining_off"
          renderValue={valueOrNone}
        />

        <PartialValue
          label="Contained Database Authentication Flag is Off"
          valuePath="contained_database_authentication_off"
          renderValue={valueOrNone}
        />

        <PartialValue
          label="Log Checkpoints Flag is On"
          valuePath="log_checkpoints_on"
          renderValue={valueOrNone}
        />

        <PartialValue
          label="Log Connections Flag is On"
          valuePath="log_connections_on"
          renderValue={valueOrNone}
        />

        <PartialValue
          label="Log Disconnections Flag is On"
          valuePath="log_disconnections_on"
          renderValue={valueOrNone}
        />

        <PartialValue
          label="Log Lock Waits Flag is On"
          valuePath="log_lock_waits_on"
          renderValue={valueOrNone}
        />

        <PartialValue
          label="Log Min Messages Flag set Appropriately"
          valuePath="log_min_messages"
          renderValue={valueOrNone}
        />

        <PartialValue
          label="Log Temp Files Flag set to 0"
          valuePath="log_temp_files_0"
          renderValue={valueOrNone}
        />

        <PartialValue
          label="Log Min Duration Statement Flag set to -1"
          valuePath="log_min_duration_statement_-1"
          renderValue={valueOrNone}
        />

        <PartialValue
          label="Authorized Networks"
          valuePath="authorized_networks"
          renderValue={valueOrNone}
        />
      </InformationsWrapper>

      <TabsMenu>
        <TabPane title="Authorized Networks">
          {renderAuthorizedNetworks(item.authorized_networks)}
        </TabPane>
      </TabsMenu>
    </Partial>
  );
};

SQLInstances.propTypes = propTypes;

export default SQLInstances;
