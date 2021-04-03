import React from 'react';
import PropTypes from 'prop-types';

import InformationsWrapper from '../../../components/InformationsWrapper';
import { Partial, PartialValue } from '../../../components/Partial';
import { partialDataShape, valueOrNone } from '../../../utils/Partials';

const propTypes = {
  data: PropTypes.shape(partialDataShape).isRequired,
};

const Images = props => {
  const { data } = props;

  if (!data) return null;

  return (
    <Partial data={data}>
      <InformationsWrapper>
        <PartialValue label="Name" valuePath="name" renderValue={valueOrNone} />

        <PartialValue
          label="Provisioning State"
          valuePath="provisioning_state"
          renderValue={valueOrNone}
        />

        <PartialValue
          label="Location"
          valuePath="location"
          renderValue={valueOrNone}
        />

        <PartialValue
          label="Hyper-V Generation"
          valuePath="hyper_vgeneration"
          renderValue={valueOrNone}
        />
      </InformationsWrapper>
    </Partial>
  );
};

Images.propTypes = propTypes;

export default Images;