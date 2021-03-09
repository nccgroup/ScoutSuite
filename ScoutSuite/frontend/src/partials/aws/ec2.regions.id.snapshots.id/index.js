import React from 'react';
import PropTypes from 'prop-types';

import { Partial, PartialValue } from '../../../components/Partial';
import { 
  partialDataShape, 
  convertBoolToEnable,
  valueOrNone,
} from '../../../utils/Partials';


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
          label="State"
          valuePath="state"
          renderValue={valueOrNone}
        />
        <PartialValue
          label="Progress"
          valuePath="progress"
          renderValue={valueOrNone}
        />
        <PartialValue
          label="Start Time"
          valuePath="start_time"
          renderValue={valueOrNone}
        />
        <PartialValue
          label="Volume"
          valuePath="volume"
        />
        <PartialValue
          label="Owner ID"
          valuePath="owner_id"
          renderValue={valueOrNone}
        />
        <PartialValue
          label="Encryption"
          valuePath="encrypted"
          renderValue={convertBoolToEnable}
        />
        <PartialValue
          label="KMS Key ID"
          valuePath="kms_key_id"
          renderValue={valueOrNone}
        />
      </div>
    </Partial>
  );
};

Ec2Snapshots.propTypes = propTypes;

export default Ec2Snapshots;
