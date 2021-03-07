import React from 'react';
import { PropTypes } from 'prop-types';

import { Partial, PartialValue } from '../../../components/Partial';
import { partialDataShape, convertBoolToEnable } from '../../../utils/Partials';

const propTypes = {
  data: PropTypes.shape(partialDataShape).isRequired,
};

const Ec2Snapshots = props => {
  const { data } = props;

  if (!data) return null;

  return (
    <Partial data={data}>
      <div className="partial-informations">
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
        />
        <PartialValue
          label="State"
          valuePath="state"
        />
        <PartialValue
          label="Progress"
          valuePath="progress"
        />
        <PartialValue
          label="Start Time"
          valuePath="start_time"
        />
        <PartialValue
          label="Volume"
          valuePath=""
        />
        <PartialValue
          label="Owner ID"
          valuePath="owner_id"
        />
        <PartialValue
          label="Encryption"
          valuePath="encrypted"
          renderValue={convertBoolToEnable}
        />
        <PartialValue
          label="KMS Key ID"
          valuePath="kms_key_id"
        />
      </div>
    </Partial>
  );
};

Ec2Snapshots.propTypes = propTypes;

export default Ec2Snapshots;
