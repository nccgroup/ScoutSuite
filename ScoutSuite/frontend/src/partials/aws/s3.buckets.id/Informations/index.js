import React from 'react';

import { PartialValue } from '../../../../components/Partial/index';
import { convertBoolToEnable } from '../../../../utils/Partials';


const Informations = () => {
  return (
    <div className="partial-informations">
      <h4>Informations</h4>
      <PartialValue 
        label="ARN" 
        valuePath="arn" 
      />
      <PartialValue 
        label="Region" 
        valuePath="region" 
      />
      <PartialValue 
        label="Creation Date" 
        valuePath="CreationDate" 
      />
      <PartialValue 
        label="Logging" 
        valuePath="logging" 
        renderValue={convertBoolToEnable} 
      />
      <PartialValue 
        label="Default Encryption" 
        valuePath="default_encryption_enabled" 
        renderValue={convertBoolToEnable} 
      />
      <PartialValue 
        label="Versioning" 
        valuePath="versioning_status_enabled"
        errorPath="versioning"
        renderValue={convertBoolToEnable} 
      />
      <PartialValue 
        label="MFA Delete" 
        valuePath="version_mfa_delete_enabled" 
        renderValue={convertBoolToEnable} 
      />
      <PartialValue 
        label="Secure Transport" 
        valuePath="secure_transport_enabled" 
        renderValue={convertBoolToEnable} 
      />
      <PartialValue 
        label="Static Web Hosting" 
        valuePath="web_hosting_enabled" 
        renderValue={convertBoolToEnable} 
      />
    </div>
  );
};

export default Informations;
