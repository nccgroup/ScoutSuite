import React from 'react';

import { PartialValue } from '../../../../components/Partial/index';
import { 
  formatDate, 
  makeTitle,
  convertBoolToEnable,
} from '../../../../utils/Partials';


const Informations = () => {
  return (
    <>
      <PartialValue 
        label="ARN" 
        valuePath="arn" 
      />
      <PartialValue 
        label="Region" 
        valuePath="region" 
      />
      <PartialValue 
        label="Engine" 
        valuePath="Engine" 
      />
      <PartialValue 
        label="Creation Time" 
        valuePath="InstanceCreateTime" 
        renderValue={formatDate}
      />
      <PartialValue 
        label="Status" 
        valuePath="DBInstanceStatus" 
        renderValue={makeTitle}
      />
      <PartialValue 
        label="Is Read Replica" 
        valuePath="is_read_replica"
      />
      <PartialValue 
        label="Auto Minor Version Upgrade" 
        valuePath="AutoMinorVersionUpgrade" 
        renderValue={convertBoolToEnable}
      />
      <PartialValue 
        label="Multi Availability Zones" 
        valuePath="MultiAZ" 
        renderValue={convertBoolToEnable}
      />
      <PartialValue 
        label="Instance Class" 
        valuePath="DBInstanceClass"
      />
      <PartialValue 
        label="Backup Retention Period" 
        valuePath="BackupRetentionPeriod"
        renderValue={value => `${value} days`}
      />
      <PartialValue 
        label="Enhanced Monitoring" 
        valuePath="EnhancedMonitoringResourceArn" 
        renderValue={convertBoolToEnable}
      />
      <PartialValue 
        label="Encrypted Storage" 
        valuePath="StorageEncrypted" 
        renderValue={convertBoolToEnable}
      />
      <PartialValue 
        label="CA Certificate" 
        valuePath="CACertificateIdentifier" 
      />
    </>
  );
};

export default Informations;
