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
      <div className="left-pane">
        <PartialValue
          label="Project ID"
          valuePath="project_id" />

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
          label="Authorized Networks"
          valuePath="authorized_networks"
          renderValue={valueOrNone}
        />
      </div>

      <TabsMenu>
        <TabPane title="Authorized Networks">{renderAuthorizedNetworks(item.authorized_networks)}</TabPane>
      </TabsMenu>
    </Partial>
  );
};

SQLInstances.propTypes = propTypes;

export default SQLInstances;
