import React from 'react';
import PropTypes from 'prop-types';

import { Partial, PartialValue } from '../../../components/Partial';
import { partialDataShape } from '../../../utils/Partials';
import InformationsWrapper from '../../../components/InformationsWrapper';

const propTypes = {
  data: PropTypes.shape(partialDataShape).isRequired,
};

const BindingsSeparationDuties = props => {
  const { data } = props;

  if (!data) return null;

  return (
    <Partial data={data}>
      <InformationsWrapper>
        <PartialValue
          label="Separation of duties enforced for service account related roles"
          valuePath="account_separation_duties" />

        <PartialValue
          label="Separation of duties enforced for KMS related roles"
          valuePath="kms_separation_duties" />

      </InformationsWrapper>
    </Partial>
  );
};

BindingsSeparationDuties.propTypes = propTypes;

export default BindingsSeparationDuties;
