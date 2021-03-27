import React from 'react';

import { PartialValue } from '../../../../components/Partial/index';


const Informations = () => {
  return (
    <>
      <h4>Informations</h4>
      <PartialValue
        label="ID"
        valuePath="id"
      />
      <PartialValue
        label="ARN"
        valuePath="arn"
      />
      <PartialValue
        label="Region"
        valuePath="region"
      />
      <PartialValue
        label="State"
        valuePath="state"
      />
      <PartialValue
        label="CIDR Block"
        valuePath="cidr_block"
      />
      <PartialValue
        label="Default"
        valuePath="default"
        renderValue={value => value.toString()}
      />
    </>
  );
};

export default Informations;