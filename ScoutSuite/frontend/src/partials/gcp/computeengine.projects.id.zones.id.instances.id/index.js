import React from 'react';
import PropTypes from 'prop-types';
import get from 'lodash/get';
import { Link } from 'react-router-dom';

import { Partial, PartialValue } from '../../../components/Partial';
import {
  partialDataShape,
  formatDate,
  convertBoolToEnable,
} from '../../../utils/Partials';
import { TabsMenu, TabPane } from '../../../components/Tabs';
import GetResourceName from '../../../components/GetResourceName';
import { valueOrNone } from '../../../utils/Partials/index';

const renderTags = tags => {
  if (!tags || tags.length === 0) return <span>None</span>;
  return (
    <div className="partial-value detailed-value">
      <span className="label">Tags</span>
      <ul>
        {Object.entries(tags).map(([key, value]) => (
          <li key={key}>
            {key}
            <ul>
              {value &&
                Array.isArray(value) &&
                value.map((v, i) => <li key={i}>{v}</li>)}
              {value && !Array.isArray(value) && <li>{value}</li>}
              {!value || (value.length === 0 && <li>None</li>)}
            </ul>
          </li>
        ))}
      </ul>
    </div>
  );
};

const renderNetworkInterfaces = network_interfaces => {
  if (!network_interfaces) return <span>None</span>;

  return (
    <ul>
      {network_interfaces.map((ni, i) => (
        <li key={i}>
          {ni.name}
          <ul>
            <li>{ni.networkIP}</li>
            <li>
              Network:{' '}
              <Link
                to={`/services/computeengine/resources/networks/${ni.network_id}`}
              >
                <GetResourceName
                  service="computeengine"
                  resource="networks"
                  id={ni.network_id}
                />
              </Link>
            </li>
            <li>
              Subnetwork:{' '}
              <Link
                to={`/services/computeengine/resources/subnetworks/${ni.subnetwork_id}`}
              >
                <GetResourceName
                  service="computeengine"
                  resource="subnetworks"
                  id={ni.subnetwork_id}
                />
              </Link>
            </li>
          </ul>
        </li>
      ))}
    </ul>
  );
};

const renderAccessScope = access_scopes => {
  if (!access_scopes) return <span>None</span>;
  return (
    <ul>
      {access_scopes.map((item, i) => (
        <li key={i}>{item}</li>
      ))}
    </ul>
  );
};

const renderDisks = (disks) => {
  if (!disks) return <span>None</span>;

  return <ul>
    {Object.values(disks).map((disk, i) => <li key={i}>
      {disk.source_device_name}
      <ul>
        <li>Bootable: {disk.bootable}</li> 
        <li>Type: {disk.type}</li>
        <li>Mode: {disk.mode}</li>
        {disk.latest_snapshot ?
          <li>Latest snapshot: {disk.latest_snapshot.creation_timestamp}</li> :
          <li>Latest snapshot: None</li>}
        <li>Customer Supplied Encryption: <span>{valueOrNone(disk.encrypted_with_csek)}</span></li>
      </ul>
    </li>)}
  </ul>;
};

const propTypes = {
  data: PropTypes.shape(partialDataShape).isRequired,
};

const Instances = props => {
  const { data } = props;
  const item = get(data, ['item'], {});

  if (!data) return null;

  return (
    <Partial data={data}>
      <div className="left-pane">
        <PartialValue
          label="Instance Name"
          valuePath="name" />

        <PartialValue
          label="Project ID"
          valuePath="project_id" />

        <PartialValue
          label="Description"
          valuePath="description" />

        <PartialValue
          label="Creation Date"
          valuePath="creation_timestamp"
          renderValue={formatDate}
        />

        <PartialValue
          label="Status"
          valuePath="status" />

        <PartialValue
          label="Deletion Protection"
          valuePath="deletion_protection_enabled"
          renderValue={convertBoolToEnable}
        />

        <PartialValue
          label="Block Project SSH Keys"
          valuePath="block_project_ssh_keys_enabled"
          renderValue={convertBoolToEnable}
        />

        <PartialValue
          label="IP Forwarding"
          valuePath="ip_forwarding_enabled"
          renderValue={convertBoolToEnable}
        />

        <PartialValue
          label="OS Login"
          valuePath="oslogin_enabled"
          renderValue={convertBoolToEnable}
        />

        <PartialValue
          label="Serial Port Connection"
          valuePath="serial_port_enabled"
          renderValue={convertBoolToEnable}
        />

        {renderTags(item.tags)}
      </div>

      <TabsMenu>
        <TabPane title="Network Interfaces">
          {renderNetworkInterfaces(item.network_interfaces)}
        </TabPane>
        <TabPane title="Identity & API Access">
          <div>
            <PartialValue
              label="Service Account"
              valuePath="service_account"
              renderValue={valueOrNone}
            />

            <PartialValue
              label="Access Scopes"
              valuePath="access_scopes"
              renderValue={renderAccessScope}
            />
          </div>
        </TabPane>
        <TabPane title="Disks">
          <div>{renderDisks(item.disks)}</div>
        </TabPane>
      </TabsMenu>
    </Partial>
  );
};

Instances.propTypes = propTypes;

export default Instances;
