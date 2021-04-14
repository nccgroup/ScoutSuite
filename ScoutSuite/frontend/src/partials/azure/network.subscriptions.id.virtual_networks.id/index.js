import React from 'react';
import PropTypes from 'prop-types';
import Accordion from '@material-ui/core/Accordion';
import AccordionSummary from '@material-ui/core/AccordionSummary';
import AccordionDetails from '@material-ui/core/AccordionDetails';
import ExpandMoreIcon from '@material-ui/icons/ExpandMore';

import InformationsWrapper from '../../../components/InformationsWrapper';
import { Partial, PartialValue } from '../../../components/Partial';
import {
  partialDataShape,
  valueOrNone,
  renderList,
} from '../../../utils/Partials';
import { TabsMenu, TabPane } from '../../../components/Partial/PartialTabs';
import Subnet from './Subnets';
import PartialSection from '../../../components/Partial/PartialSection/index';

const renderSubnets = subnets => {
  return Object.entries(subnets).map(([key, subnet]) => (
    <Accordion
      square variant="outlined"
      key={key}>
      <AccordionSummary
        expandIcon={<ExpandMoreIcon />}
        aria-controls="panel1a-content"
        id="panel1a-header"
      >
        <span>{subnet.name}</span>
      </AccordionSummary>
      <AccordionDetails>
        <PartialSection path={`subnets.${key}`}>
          <Subnet subnet={subnet} />
        </PartialSection>
      </AccordionDetails>
    </Accordion>
  ));
};

const propTypes = {
  data: PropTypes.shape(partialDataShape).isRequired,
  item: PropTypes.object,
};

const VirtualNetworks = props => {
  const { data, item } = props;

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
        <TabPane title="Subnets">{renderSubnets(item.subnets)}</TabPane>
      </TabsMenu>
    </Partial>
  );
};

VirtualNetworks.propTypes = propTypes;

export default VirtualNetworks;
