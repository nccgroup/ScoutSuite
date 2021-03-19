import React from 'react';

import { PartialValue, PartialSection } from '../../../../components/Partial/index';
import { convertBoolToEnable, formatDate } from '../../../../utils/Partials';


const Informations = () => {
  return (
    <>
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
        renderValue={formatDate}
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

      <PartialSection path="public_access_block_configuration">
        <h4>Public Access Block Configuration</h4>
        <PartialValue 
          label="Ignore Public ACLs" 
          valuePath="IgnorePublicAcls" 
          renderValue={convertBoolToEnable} 
        />
        <PartialValue 
          label="Block Public Policies" 
          valuePath="BlockPublicPolicy" 
          renderValue={convertBoolToEnable} 
        />
        <PartialValue 
          label="Block Public ACLs" 
          valuePath="BlockPublicAcls" 
          renderValue={convertBoolToEnable} 
        />
        <PartialValue 
          label="Restrict Public Buckets" 
          valuePath="RestrictPublicBuckets" 
          renderValue={convertBoolToEnable} 
        />
      </PartialSection>

    </>
  );
};

export default Informations;
