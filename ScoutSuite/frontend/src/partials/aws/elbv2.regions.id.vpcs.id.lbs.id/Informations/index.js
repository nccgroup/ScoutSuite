import React from 'react';

import { PartialValue } from '../../../../components/Partial';


const Informations = () => {
  return (
    <>
      <PartialValue
        label="ARN"
        valuePath="arn"
      />
      <PartialValue
        label="VPC"
        valuePath="vpc"
      />
      <PartialValue
        label="DNS"
        valuePath="DNSName"
      />
      <PartialValue
        label="Scheme"
        valuePath="Scheme"
        errorPath="load_balancer_scheme"
      />
      <PartialValue
        label="Type"
        valuePath="Type"
      />
      <PartialValue
        label="Availability zones"
        valuePath="AvailabilityZones"
        renderValue={value => (
          <ul>
            {value.map((zone, i) => (
              <li key={i}>
                {`${zone.ZoneName} (${zone.SubnetId})`}
              </li>
            ))}
          </ul>
        )}
      />
    </>
  );
};

export default Informations;
