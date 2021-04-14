import React, { useMemo } from 'react';
import PropTypes from 'prop-types';
// import Skeleton from '@material-ui/lab/Skeleton';

import InformationsWrapper from '../../../components/InformationsWrapper';
import { Partial, PartialValue } from '../../../components/Partial';
import {
  partialDataShape,
  valueOrNone,
  renderList,
} from '../../../utils/Partials';
import { TabsMenu, TabPane } from '../../../components/Partial/PartialTabs';
import ResourceLink from '../../../components/ResourceLink/index';

const renderNetworkInterfaces = id => {
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

const Instances = props => {
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
          label="VM ID"
          valuePath="vm_id"
          renderValue={valueOrNone}
        />

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
          label="Identity Principal ID"
          valuePath="identity.principal_id"
          errorPath="identity"
          renderValue={valueOrNone}
        />

        <PartialValue
          label="License Type"
          valuePath="license_type"
          renderValue={valueOrNone}
        />

        <PartialValue
          label="Plan" valuePath="plan"
          renderValue={valueOrNone} />

        <PartialValue
          label="Zones"
          valuePath="zones"
          renderValue={valueOrNone}
        />

        <PartialValue
          label="Instance View"
          valuePath="instance_view"
          renderValue={valueOrNone}
        />

        <PartialValue
          label="Proximity Placement Group"
          valuePath="proximity_placement_group"
          renderValue={valueOrNone}
        />

        <PartialValue
          label="Availability Set"
          valuePath="availability_set"
          renderValue={valueOrNone}
        />

        <PartialValue
          label="Additional Capabilities"
          valuePath="additional_capabilities"
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
        <TabPane title="Network Interfaces">
          {renderList(network_interfaces_ids, '', value =>
            renderNetworkInterfaces(value),
          )}
        </TabPane>

        <TabPane title="Extensions">
          {renderList(item.extensions)}
        </TabPane>
      </TabsMenu>
    </Partial>
  );
};

Instances.propTypes = propTypes;

export default Instances;
