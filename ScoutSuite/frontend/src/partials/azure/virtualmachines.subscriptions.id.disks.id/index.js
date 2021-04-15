import React from 'react';
import PropTypes from 'prop-types';

import InformationsWrapper from '../../../components/InformationsWrapper';
import { Partial, PartialValue } from '../../../components/Partial';
import {
  partialDataShape,
  valueOrNone,
  formatDate,
} from '../../../utils/Partials';

const propTypes = {
  data: PropTypes.shape(partialDataShape).isRequired,
};

const Disks = props => {
  const { data } = props;

  if (!data) return null;

  return (
    <Partial data={data}>
      <InformationsWrapper>
        <PartialValue
          label="Name" valuePath="name"
          renderValue={valueOrNone} />

        <PartialValue
          label="Unique ID"
          valuePath="unique_id"
          renderValue={valueOrNone}
        />

        <PartialValue
          label="Location"
          valuePath="location"
          renderValue={valueOrNone}
        />

        <PartialValue
          label="Time Created"
          valuePath="time_created"
          renderValue={formatDate}
        />

        <PartialValue
          label="Provisioning State"
          valuePath="provisioning_state"
          renderValue={valueOrNone}
        />

        <PartialValue
          label="Disk State"
          valuePath="disk_state"
          renderValue={valueOrNone}
        />

        <PartialValue
          label="Zones"
          valuePath="zones"
          renderValue={valueOrNone}
        />

        <PartialValue
          label="Encryption Type"
          valuePath="encryption_type"
          renderValue={valueOrNone}
        />

        <PartialValue
          label="OS Type"
          valuePath="os_type"
          renderValue={valueOrNone}
        />

        <PartialValue
          label="Hyper V Generation"
          valuePath="hyper_vgeneration"
          renderValue={valueOrNone}
        />

        <PartialValue
          label="Disk Size GB"
          valuePath="disk_size_gb"
          renderValue={valueOrNone}
        />
      </InformationsWrapper>
    </Partial>
  );
};

Disks.propTypes = propTypes;

export default Disks;
