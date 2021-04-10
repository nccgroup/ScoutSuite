import React from 'react';

import { PartialValue } from '../../../../components/Partial';


const Informations = () => {
  return (
    <>
      <PartialValue
        label="Region"
        valuePath="region"
      />
      <PartialValue
        label="VPC"
        valuePath="vpc"
      />
      <PartialValue
        label="ID"
        valuePath="id"
      />
      <PartialValue
        label="Availability Zone"
        valuePath="Ec2InstanceAttributes.Ec2AvailabilityZone"
      />
      <PartialValue
        label="Status"
        valuePath="Status.State"
      />
      <PartialValue
        label="Instance Profile"
        valuePath="Ec2InstanceAttributes.IamInstanceProfile"
      />
      <PartialValue
        label="Visibile to all users"
        valuePath="VisibleToAllUsers"
      />
    </>
  );
};

export default Informations;
