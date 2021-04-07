import React from 'react';
import PropTypes from 'prop-types';

import InformationsWrapper from '../../../components/InformationsWrapper';
import { Partial, PartialValue } from '../../../components/Partial';
import { partialDataShape } from '../../../utils/Partials';

const propTypes = {
  data: PropTypes.shape(partialDataShape).isRequired,
};

const AutoProvisioningSettings = props => {
  const { data } = props;

  if (!data) return null;

  return (
    <Partial data={data}>
      <InformationsWrapper>
        <PartialValue label="Name" valuePath="name" />

        <PartialValue label="Auto Provisioning" valuePath="auto_provision" />
      </InformationsWrapper>
    </Partial>
  );
};

AutoProvisioningSettings.propTypes = propTypes;

export default AutoProvisioningSettings;
