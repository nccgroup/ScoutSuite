import React from 'react';

import { PartialValue } from '../../../../components/Partial/index';


const Informations = () => {
  return (
    <>
      <PartialValue label="ID" valuePath="id" />
      <PartialValue label="ARN" valuePath="arn" />
      <PartialValue label="Region" valuePath="region" />
      <PartialValue label="VPC" valuePath="vpc" />
      <PartialValue label="Description" valuePath="description" />
    </>
  );
};

export default Informations;
