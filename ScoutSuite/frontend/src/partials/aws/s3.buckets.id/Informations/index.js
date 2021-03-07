import React from 'react';

import { PartialValue } from '../../../../components/Partial/index';
import { convertBoolToEnable } from '../../../../utils/Partials';


const Informations = () => {
  return (
    <div className="partial-informations">
      <h4>Informations</h4>
      <PartialValue label="ARN" path="arn" />
      <PartialValue label="Region" path="region" />
      <PartialValue label="Creation Date" path="CreationDate" />
      <PartialValue 
        label="Logging" 
        path="logging" 
        renderValue={convertBoolToEnable} 
      />
      <PartialValue 
        label="Default Encryption" 
        path="default_encryption_enabled" 
        renderValue={convertBoolToEnable} 
      />
      <PartialValue 
        label="Versioning" 
        path="versioning_status_enabled"
        errorPath="versioning"
        renderValue={convertBoolToEnable} 
      />
      <PartialValue 
        label="MFA Delete" 
        path="version_mfa_delete_enabled" 
        renderValue={convertBoolToEnable} 
      />
      <PartialValue 
        label="Secure Transport" 
        path="secure_transport_enabled" 
        renderValue={convertBoolToEnable} 
      />
      <PartialValue 
        label="Static Web Hosting" 
        path="web_hosting_enabled" 
        renderValue={convertBoolToEnable} 
      />
    </div>
  );
};

export default Informations;
