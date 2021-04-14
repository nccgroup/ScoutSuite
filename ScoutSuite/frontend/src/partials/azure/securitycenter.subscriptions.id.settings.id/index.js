import React from 'react';
import PropTypes from 'prop-types';

import InformationsWrapper from '../../../components/InformationsWrapper';
import { Partial, PartialValue } from '../../../components/Partial';
import { partialDataShape } from '../../../utils/Partials';

const propTypes = {
  data: PropTypes.shape(partialDataShape).isRequired,
};

const SecuritySettings = props => {

  const { data } = props;

  if (!data) return null;

  return (
    <Partial data={data}>
      <InformationsWrapper>
        <PartialValue label="Name" valuePath="name" />
        <PartialValue label="Kind" valuePath="kind" />
        <PartialValue label="Enabled" valuePath="enabled" />
      </InformationsWrapper>
    </Partial>
  );
};

SecuritySettings.propTypes = propTypes;

export default SecuritySettings;
