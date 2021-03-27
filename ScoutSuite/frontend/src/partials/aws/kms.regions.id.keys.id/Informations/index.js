import React from 'react';

import { PartialValue } from '../../../../components/Partial/index';
import { 
  formatDate, 
  valueOrNone,
  convertBoolToEnable,
} from '../../../../utils/Partials';


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
        label="Status" 
        valuePath="key_enabled"
        renderValue={convertBoolToEnable}
      />
      <PartialValue 
        label="Origin" 
        valuePath="origin"
        renderValue={valueOrNone}
      />
      <PartialValue 
        label="Key Manager" 
        valuePath="key_manager"
        renderValue={valueOrNone}
      />
      <PartialValue 
        label="Rotation" 
        valuePath="rotation_enabled"
        renderValue={convertBoolToEnable}
      />
    </>
  );
};

export default Informations;
