import React from 'react';
import PropTypes from 'prop-types';

import InformationsWrapper from '../../../components/InformationsWrapper';
import { Partial, PartialValue } from '../../../components/Partial';
import { partialDataShape } from '../../../utils/Partials';

const propTypes = {
  data: PropTypes.shape(partialDataShape).isRequired,
};

const DiagnosticSettings = props => {

  const { data } = props;

  if (!data) return null;

  return (
    <Partial data={data}>
      <InformationsWrapper>
        <PartialValue label="Diagnostic setting exists" valuePath="diagnostic_exist" />
      </InformationsWrapper>
    </Partial>
  );
};

DiagnosticSettings.propTypes = propTypes;

export default DiagnosticSettings;
