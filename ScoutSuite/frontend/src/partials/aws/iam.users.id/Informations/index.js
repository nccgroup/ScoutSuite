import React from 'react';

import { PartialValue } from '../../../../components/Partial/index';
import { formatDate, valueOrNone } from '../../../../utils/Partials';


const Informations = () => {
  return (
    <>
      <h4>Informations</h4>
      <PartialValue 
        label="ARN" 
        valuePath="arn"
        renderValue={valueOrNone}
      />
      <PartialValue 
        label="Creation Date" 
        valuePath="CreateDate"
        renderValue={formatDate}
      />
    </>
  );
};

export default Informations;
