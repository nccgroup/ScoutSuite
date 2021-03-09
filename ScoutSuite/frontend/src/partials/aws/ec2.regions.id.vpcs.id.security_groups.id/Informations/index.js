import React from 'react';

import { PartialValue } from '../../../../components/Partial/index';


const Informations = () => {
  return (
    <div className="partial-informations">
      <h4>Informations</h4>
      <PartialValue label="ID" valuePath="id" />
      <PartialValue label="ARN" valuePath="arn" />
      <PartialValue label="Region" valuePath="region" />
      {/* TODO: Get VPC value from 'services.vpc.regions'*/}
      <PartialValue label="VPC" valuePath="vpc" />  
      <PartialValue label="Description" valuePath="description" />
    </div>
  );
};

export default Informations;
