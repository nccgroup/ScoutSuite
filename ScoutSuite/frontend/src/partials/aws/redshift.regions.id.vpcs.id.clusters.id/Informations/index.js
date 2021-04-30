import React from 'react';

import { PartialValue } from '../../../../components/Partial/index';
import { formatDate } from '../../../../utils/Partials';


const Informations = () => {
  return (
    <>
      <PartialValue 
        label="ARN" 
        valuePath="arn" 
      />
      <PartialValue 
        label="Node Type" 
        valuePath="NodeType" 
      />
      <PartialValue 
        label="Allow Version Upgrade" 
        valuePath="AllowVersionUpgrade" 
      />
      <PartialValue 
        label="Automated Snapshot Retention Period" 
        valuePath="AutomatedSnapshotRetentionPeriod"
      />
      <PartialValue 
        label="Creation Time" 
        valuePath="ClusterCreateTime" 
        renderValue={formatDate}
      />
      <PartialValue 
        label="Availability Zone" 
        valuePath="AvailabilityZone"
      />
      <PartialValue 
        label="Encrypted" 
        valuePath="Encrypted"
      />
      <PartialValue 
        label="Cluster Parameter Groups" 
        valuePath="ClusterParameterGroups" 
        renderValue={value => (
          <ul>
            {value.map((group, i) => (
              <li key={i}>
                {group.ParameterGroupName}
              </li>
            ))}
          </ul>
        )}
      />
    </>
  );
};

export default Informations;
