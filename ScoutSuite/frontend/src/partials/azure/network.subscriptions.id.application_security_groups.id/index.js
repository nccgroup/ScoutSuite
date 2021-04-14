import React, { useMemo } from 'react';
import PropTypes from 'prop-types';

import InformationsWrapper from '../../../components/InformationsWrapper';
import { Partial, PartialValue } from '../../../components/Partial';
import {
  partialDataShape,
  valueOrNone,
  renderList,
} from '../../../utils/Partials';
import { TabsMenu, TabPane } from '../../../components/Partial/PartialTabs';
import ResourceLink from '../../../components/ResourceLink/index';

const renderNetworkInterface = id => {
  return (
    <ResourceLink
      service="network" 
      resource="network_interfaces"
      id={id} />
  );
};

const propTypes = {
  data: PropTypes.shape(partialDataShape).isRequired,
  item: PropTypes.object,
};

const AppSecurityGroups = props => {
  const { data, item } = props;
  const network_interfaces_ids = useMemo(
    () => Object.values(item.network_interfaces).map(item => item.id),
    [item.network_interfaces],
  );

  if (!data) return null;

  return (
    <Partial data={data}>
      <InformationsWrapper>
        <PartialValue
          label="Name" valuePath="name"
          renderValue={valueOrNone} />

        <PartialValue
          label="Location"
          valuePath="location"
          renderValue={valueOrNone}
        />

        <PartialValue
          label="Provisioning State"
          valuePath="provisioning_state"
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
        <TabPane title="Attached Network Interfaces">
          {renderList(network_interfaces_ids, '', value =>
            renderNetworkInterface(value),
          )}
        </TabPane>
      </TabsMenu>
    </Partial>
  );
};

AppSecurityGroups.propTypes = propTypes;

export default AppSecurityGroups;
