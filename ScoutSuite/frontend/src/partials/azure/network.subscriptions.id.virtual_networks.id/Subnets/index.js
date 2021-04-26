import React from 'react';
import PropTypes from 'prop-types';

import { PartialValue } from '../../../../components/Partial';
import { valueOrNone, renderList } from '../../../../utils/Partials';
import ResourceLink from '../../../../components/ResourceLink/index';

const renderInstances = instances => {
  const renderInstanceLink = (id) => (
    <ResourceLink
      service="virtualmachines"
      resource="instances"
      id={id} />
  );

  return renderList(instances, '', value => renderInstanceLink(value));
};

const propTypes = {
  subnet: PropTypes.object.isRequired,
};

const Subnets = props => {
  const { subnet } = props;

  return (
    <div>
      <PartialValue
        label="Address Prefix"
        valuePath="address_prefix"
        renderValue={valueOrNone}
      />

      <PartialValue
        label="Address Prefixes"
        valuePath="address_prefixes"
        renderValue={valueOrNone}
      />

      <PartialValue
        label="Provisioning State"
        valuePath="provisioning_state"
        renderValue={valueOrNone}
      />

      <PartialValue
        label="Route Table"
        valuePath="route_table"
        renderValue={valueOrNone}
      />

      <PartialValue
        label="Interface Endpoints"
        valuePath="interface_endpoints"
        renderValue={valueOrNone}
      />

      <PartialValue
        label="IP Configuration Profiles"
        valuePath="ip_configuration_profiles"
        renderValue={valueOrNone}
      />

      <PartialValue
        label="Service Endpoints"
        valuePath="service_endpoints"
        renderValue={valueOrNone}
      />

      <PartialValue
        label="Service Endpoint Policies"
        valuePath="service_endpoint_policies"
        renderValue={valueOrNone}
      />

      <PartialValue
        label="Service Association Links"
        valuePath="service_association_links"
        renderValue={valueOrNone}
      />

      <PartialValue
        label="Resource Navigation Links"
        valuePath="resource_navigation_links"
        renderValue={valueOrNone}
      />

      <PartialValue
        label="Delegations"
        valuePath="delegations"
        renderValue={valueOrNone}
      />

      <PartialValue
        label="Purpose"
        valuePath="purpose"
        renderValue={valueOrNone}
      />

      <br />

      <h5>Instances</h5>

      {renderInstances(subnet.instances)}
    </div>
  );
};

Subnets.propTypes = propTypes;

export default Subnets;
