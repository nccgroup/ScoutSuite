import React from 'react';
import PropTypes from 'prop-types';

import InformationsWrapper from '../../../components/InformationsWrapper';
import { Partial, PartialValue } from '../../../components/Partial';
import { convertBoolToEnable, partialDataShape } from '../../../utils/Partials';

const propTypes = {
  data: PropTypes.shape(partialDataShape).isRequired,
};

const RessourcesLogging = props => {

  const { data } = props;

  if (!data) return null;

  return (
    <Partial data={data}>
      <InformationsWrapper>
        <PartialValue
          label="Logging for key vault enabled"
          valuePath="diagnostic_key_vault.audit_event_enabled"
          errorPath="diagnostic_key_vault_audit_event_enabled"
          renderValue={convertBoolToEnable} />
      </InformationsWrapper>
    </Partial>
  );
};

RessourcesLogging.propTypes = propTypes;

export default RessourcesLogging;
