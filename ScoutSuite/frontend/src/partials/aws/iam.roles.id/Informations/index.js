import React from 'react';

import { PartialValue } from '../../../../components/Partial/index';
import { formatDate, valueOrNone } from '../../../../utils/Partials';


const Informations = () => {
  return (
    <>
      <PartialValue 
        label="ID" 
        valuePath="id"
        renderValue={valueOrNone}
      />
      <PartialValue 
        label="ARN" 
        valuePath="arn"
        renderValue={valueOrNone}
      />
      <PartialValue 
        label="Description" 
        valuePath="description"
        renderValue={valueOrNone}
      />
      <PartialValue 
        label="Creation Date" 
        valuePath="CreateDate"
        renderValue={formatDate}
      />
      <PartialValue 
        label="Path" 
        valuePath="path"
        renderValue={valueOrNone}
      />
      <PartialValue 
        label="Max Session Duration" 
        valuePath="max_session_duration"
        renderValue={valueOrNone}
      />
    </>
  );
};

export default Informations;
