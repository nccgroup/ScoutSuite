import React from 'react';
import PropTypes from 'prop-types';
import get from 'lodash/get';
import sortBy from 'lodash/sortBy';

import InformationsWrapper from '../../../components/InformationsWrapper';
import { Partial, PartialValue } from '../../../components/Partial';
import {
  partialDataShape,
  renderList,
  valueOrNone,
} from '../../../utils/Partials';
import { TabsMenu, TabPane } from '../../../components/Partial/PartialTabs';
import GetResourceLink from '../../../components/GetResourceLink';

const renderSecurityRules = items => {
  return (
    <div className="table-responsive">
      <table className="table">
        <thead>
          <tr>
            <td>Priority</td>
            <td>Name</td>
            <td>Protocol</td>
            <td>Source Port</td>
            <td>Source Filter</td>
            <td>Destination Port</td>
            <td>Destination Filter</td>
            <td>Action</td>
          </tr>
        </thead>
        <tbody>
          {items.map(item => (
            <tr key={item.name}>
              <td width="10%" className="text-center">
                {item.priority}
              </td>
              <td width="40%">{item.name}</td>
              <td width="10%" className="text-center">
                {item.protocol}
              </td>
              <td width="10%" className="text-center">
                {item.source_port_ranges}
              </td>
              {item.source_address_prefixes_is_asg && (
                <td width="10%" className="text-center">
                  <GetResourceLink
                    service="network"
                    resource="application_security_groups"
                    id={item.source_address_prefixes}
                  />
                </td>
              )}
              {!item.source_address_prefixes_is_asg && (
                <td width="10%" className="text-center">
                  {item.source_address_prefixes}
                </td>
              )}
              <td width="10%" className="text-center">
                {item.destination_port_ranges}
              </td>
              <td width="10%" className="text-center">
                {item.destination_address_prefixes}
              </td>
              <td width="10%" className="text-center">
                {item.allow && (
                  <i className="fa fa-check-circle finding-good"></i>
                )}
                {!item.allow && (
                  <i className="fa fa-times-circle finding-danger"></i>
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

const renderSubnetLink = ({id}) => (
  <GetResourceLink
    service="network" resource="virtual_networks"
    id={id} />
);

const propTypes = {
  data: PropTypes.shape(partialDataShape).isRequired,
};

const SecurityGroups = props => {
  const { data } = props;
  const item = get(data, ['item'], {});

  if (!data) return null;

  const sortedSecurityRules = sortBy(item.security_rules, 'priority');
  const inbound = sortedSecurityRules.filter(
    ({ direction }) => direction === 'Inbound',
  );
  const outbound = sortedSecurityRules.filter(
    ({ direction }) => direction === 'Outbound',
  );

  return (
    <Partial data={data}>
      <InformationsWrapper>
        <PartialValue label="Name" valuePath="name" />

        <PartialValue label="Location" valuePath="location" />

        <PartialValue label="State" valuePath="provisioning_state" />

        <PartialValue
          label="Tags"
          valuePath="tags"
          renderValue={tags => renderList(tags, valueOrNone)}
        />

        <PartialValue
          label="Resource group"
          valuePath="resource_group_name"
          renderValue={valueOrNone}
        />
      </InformationsWrapper>

      <TabsMenu>
        <TabPane title="Inbound Security Rules">
          {renderSecurityRules(inbound)}
        </TabPane>

        <TabPane title="Outbound Security Rules">
          {renderSecurityRules(outbound)}
        </TabPane>

        <TabPane title="Attached Subnets">
          <PartialValue
            valuePath="subnets"
            renderValue={subnets => renderList(Object.values(subnets), '', renderSubnetLink)}
          />
        </TabPane>

        <TabPane title="Attached Network Interfaces">
          {/* ADD NETWORK INTERFACES */}
        </TabPane>
      </TabsMenu>
    </Partial>
  );
};

SecurityGroups.propTypes = propTypes;

export default SecurityGroups;
