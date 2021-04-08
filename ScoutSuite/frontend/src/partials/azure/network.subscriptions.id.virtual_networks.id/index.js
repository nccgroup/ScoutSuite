import React from 'react';
import PropTypes from 'prop-types';

import InformationsWrapper from '../../../components/InformationsWrapper';
import { Partial, PartialValue } from '../../../components/Partial';
import {
  partialDataShape,
  valueOrNone,
  renderList,
} from '../../../utils/Partials';
import { TabsMenu, TabPane } from '../../../components/Partial/PartialTabs';


const propTypes = {
  data: PropTypes.shape(partialDataShape).isRequired,
};

const VirtualNetworks = props => {
  const { data } = props;

  if (!data) return null;

  return (
    <Partial data={data}>
      <InformationsWrapper>
        <PartialValue label="Name" valuePath="name" />

        <PartialValue label="Resource GUID" valuePath="resource_guid" />

        <PartialValue label="Type" valuePath="type" />

        <PartialValue label="Location" valuePath="location" />

        <PartialValue
          label="Provisioning State"
          valuePath="provisioning_state"
        />

        <PartialValue
          label="Address Space"
          valuePath="address_space.address_prefixes"
          errorPath="address_space"
        />

        <PartialValue
          label="DHCP Options"
          valuePath="dhcp_options"
          renderValue={valueOrNone}
        />

        <PartialValue
          label="Virtual Network Peerings"
          valuePath="virtual_network_peerings"
          renderValue={valueOrNone}
        />

        <PartialValue
          label="Enable VM Protection"
          valuePath="enable_vm_protection"
        />

        <PartialValue
          label="Enable DDoS Protection"
          valuePath="enable_ddos_protection"
        />

        <PartialValue
          label="DDoS Protection Plan"
          valuePath="ddos_protection_plan"
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
        <TabPane title="Subnets">
          {/* RENDER SUBNET */} 
        </TabPane>
      </TabsMenu>
    </Partial>
  );
};

VirtualNetworks.propTypes = propTypes;

export default VirtualNetworks;
