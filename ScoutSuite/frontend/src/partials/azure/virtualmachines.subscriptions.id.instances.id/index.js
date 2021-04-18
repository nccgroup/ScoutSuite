import React from 'react';
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
import DetailedValue from '../../../components/DetailedValue';

const renderNetworkInterfaces = id => {
  return (
    <ResourceLink
      service="network" 
      resource="network_interfaces"
      id={id} />
  );
};

const renderKeyValue = ([key, value]) => {
  return <DetailedValue
    label={key}
    value={valueOrNone(value)} />;
};

const renderExtension = (item) => {
  return <PartialValue
    label=''
    value={item.name}
    errorPath="extensions" />;
};

const propTypes = {
  data: PropTypes.shape(partialDataShape).isRequired,
  item: PropTypes.object,
};

const Instances = props => {
  const { data, item } = props;

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

        <TabPane title="Diagnostics Profile" disabled={!item.diagnostics_profile}>
          {item.diagnostics_profile && renderList(Object.entries(item.diagnostics_profile), '', item =>
            renderKeyValue(item)
          )}
        </TabPane>

        <TabPane title="OS Profile" disabled={!item.os_profile}>
          {item.os_profile && renderList(Object.entries(item.os_profile), '', item =>
            renderKeyValue(item)
          )}
        </TabPane>

        <TabPane title="Storage Profile" disabled={!item.storage_profile}>
          {item.storage_profile && renderList(Object.entries(item.storage_profile), '', item =>
            renderKeyValue(item)
          )}
        </TabPane>

        <TabPane title="Additional Capabilities" disabled={!item.additional_capabilities}>
          {item.additional_capabilities && renderList(Object.entries(item.additional_capabilities), '', item =>
            valueOrNone(item)
          )}
        </TabPane>

        <TabPane title="Network Interfaces">
          {renderList(item.network_interfaces, '', id =>
            renderNetworkInterfaces(id)
          )}
        </TabPane>

        <TabPane title="Extensions">
          {renderList(item.extensions, '', value => renderExtension(value))}
        </TabPane>
      </TabsMenu>
    </Partial>
  );
};

Instances.propTypes = propTypes;

export default Instances;
