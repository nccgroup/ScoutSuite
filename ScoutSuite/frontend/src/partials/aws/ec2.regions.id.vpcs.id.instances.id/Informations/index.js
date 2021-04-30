import React from 'react';

import { PartialValue } from '../../../../components/Partial';
import { 
  valueOrNone,
  convertBoolToEnable,
  formatDate,
} from '../../../../utils/Partials';


const Informations = () => {
  return (
    <>
      <PartialValue
        label="ARN"
        valuePath="arn"
      />
      <PartialValue
        label="ID"
        valuePath="id"
      />
      <PartialValue
        label="Region"
        valuePath="region"
      />
      <PartialValue
        label="Availability Zone"
        valuePath="availability_zone"
      />
      <PartialValue
        label="VPC"
        valuePath="vpc"
      />
      <PartialValue
        label="Reservation ID"
        valuePath="reservation_id"
      />
      <PartialValue
        label="IAM role"
        valuePath="iam_role"
        renderValue={valueOrNone}
      />
      <PartialValue
        label="Monitoring"
        valuePath="monitoring_enabled"
        renderValue={convertBoolToEnable}
      />
      <PartialValue
        label="Access Key Name"
        valuePath="KeyName"
      />
      <PartialValue
        label="State"
        valuePath="State.Name"
      />
      <PartialValue
        label="Instance Type"
        valuePath="InstanceType"
      />
      <PartialValue
        label="Up Since"
        valuePath="LaunchTime"
        renderValue={formatDate}
      />
    </>
  );
};

export default Informations;
