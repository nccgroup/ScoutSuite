import React from 'react';
import PropTypes from 'prop-types';
import get from 'lodash/get';

import InformationsWrapper from '../../../components/InformationsWrapper';
import { Partial, PartialValue } from '../../../components/Partial';
import {
  partialDataShape,
  valueOrNone,
  renderList,
} from '../../../utils/Partials';
import { TabsMenu, TabPane } from '../../../components/Partial/PartialTabs';
import ResourceLink from '../../../components/ResourceLink/index';
import { useAPI } from '../../../api/useAPI';
import { getResourceEndpoint } from '../../../api/paths';

const renderNetworkSG = id => {
  return <ResourceLink
    services="network" resource="security_groups"
    id={id} />;
};

const renderSubnet = (subnet, virtual_network) => {
  if (!virtual_network) return <span>None</span>;
  const subnetName = virtual_network.subnets[subnet.id].name;

  return (
    <ResourceLink
      service="network"
      resource="virtual_networks"
      id={subnet.virtual_network_id}
      name={subnetName}
    />
  );
};

const renderAppSGLinks = ids => {
  const renderAppSGLink = id => (
    <ResourceLink
      service="network"
      resource="application_security_groups"
      id={id}
    />
  );

  return renderList(ids, '', id => renderAppSGLink(id));
};

const propTypes = {
  data: PropTypes.shape(partialDataShape).isRequired,
  item: PropTypes.object,
};

const NetworkInterfaces = props => {
  const { data, item } = props;
  const virtual_network_id = get(item, [
    'ip_configuration',
    'subnet',
    'virtual_network_id',
  ]);
  const { data: virtual_network } = useAPI(
    getResourceEndpoint('network', 'virtual_networks', virtual_network_id),
  );

  if (!data) return null;

  return (
    <Partial data={data}>
      <InformationsWrapper>
        <PartialValue
          label="Provisioning State"
          valuePath="provisioning_state"
          renderValue={valueOrNone}
        />

        <PartialValue
          label="Primary"
          valuePath="primary"
          renderValue={valueOrNone}
        />

        <PartialValue
          label="IP Configurations"
          valuePath="ip_configurations"
          renderValue={valueOrNone}
        />

        <PartialValue
          label="Mac Address"
          valuePath="mac_address"
          renderValue={valueOrNone}
        />

        <PartialValue
          label="Interface Endpoint"
          valuePath="interface_endpoint"
          renderValue={valueOrNone}
        />

        <PartialValue
          label="Network Security Group"
          valuePath="network_security_group"
          renderValue={value =>
            value ? renderNetworkSG(value) : <span>None</span>
          }
        />

        <PartialValue
          label="Enable IP Forwarding"
          valuePath="enable_ip_forwarding"
          renderValue={valueOrNone}
        />

        <PartialValue
          label="Enable Accelerated Networking"
          valuePath="enable_accelerated_networking"
          renderValue={valueOrNone}
        />

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
        <TabPane title="IP Configuration">
          <PartialValue
            label="Name"
            valuePath="ip_configuration.name"
            renderValue={valueOrNone}
          />

          <PartialValue
            label="Provisioning State"
            valuePath="ip_configuration.provisioning_state"
            renderValue={valueOrNone}
          />

          <PartialValue
            label="Primary"
            valuePath="ip_configuration.primary"
            renderValue={valueOrNone}
          />

          <PartialValue
            label="Public IP Address"
            valuePath="ip_configuration.public_ip_address.ip_address"
            errorPath="ip_configuration.public_ip_address"
            renderValue={valueOrNone}
          />

          <PartialValue
            label="Private IP Address"
            valuePath="ip_configuration.private_ip_address"
            renderValue={valueOrNone}
          />

          <PartialValue
            label="Private IP Allocation Method"
            valuePath="ip_configuration.private_ip_allocation_method"
            renderValue={valueOrNone}
          />

          <PartialValue
            label="Private IP Address Version"
            valuePath="ip_configuration.private_ip_address_version"
            renderValue={valueOrNone}
          />

          <PartialValue
            label="Subnet"
            valuePath="ip_configuration.subnet"
            renderValue={subnet => renderSubnet(subnet, virtual_network)}
          />

          <PartialValue
            label="Application Security Groups"
            valuePath="ip_configuration.application_security_groups"
            renderValue={value => renderAppSGLinks(value)}
          />

          <PartialValue
            label="Application Gateway Backend Address Pools"
            valuePath="ip_configuration.application_gateway_backend_address_pools"
            renderValue={valueOrNone}
          />

          <PartialValue
            label="Load Balancer Backend Address Pools"
            valuePath="ip_configuration.load_balancer_backend_address_pools"
            renderValue={valueOrNone}
          />

          <PartialValue
            label="Load Balancer Inbound NAT Rules"
            valuePath="ip_configuration.load_balancer_inbound_nat_rules"
            renderValue={valueOrNone}
          />

          <PartialValue
            label="Virtual Network Taps"
            valuePath="ip_configuration.virtual_network_taps"
            renderValue={valueOrNone}
          />
        </TabPane>
      </TabsMenu>
    </Partial>
  );
};

NetworkInterfaces.propTypes = propTypes;

export default NetworkInterfaces;
