import React from 'react';
import PropTypes from 'prop-types';

import InformationsWrapper from '../../../components/InformationsWrapper';
import { Partial, PartialValue } from '../../../components/Partial';
import { partialDataShape, valueOrNone } from '../../../utils/Partials';
import { TabsMenu, TabPane } from '../../../components/Partial/PartialTabs';

const propTypes = {
  data: PropTypes.shape(partialDataShape).isRequired,
};

const Instances = props => {
  const { data } = props;

  if (!data) return null;

  return (
    <Partial data={data}>
      <InformationsWrapper>
        <PartialValue label="Name" valuePath="name" renderValue={valueOrNone} />

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

        <PartialValue label="Plan" valuePath="plan" renderValue={valueOrNone} />

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
          renderValue={} />

        <PartialValue
          label="Resource group"
          valuePath="resource_group_name"
          renderValue={valueOrNone}
        />
      </InformationsWrapper>

      <TabsMenu>
        <TabPane title="Network Interfaces"></TabPane>

        <TabPane title="Extensions"></TabPane>
      </TabsMenu>
    </Partial>
  );
};

Instances.propTypes = propTypes;

export default Instances;
