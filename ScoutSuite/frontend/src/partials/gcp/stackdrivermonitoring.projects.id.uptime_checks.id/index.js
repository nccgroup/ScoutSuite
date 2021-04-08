import React from 'react';
import PropTypes from 'prop-types';

import { Partial, PartialValue } from '../../../components/Partial';
import { partialDataShape, valueOrNone } from '../../../utils/Partials';
import InformationsWrapper from '../../../components/InformationsWrapper';

const propTypes = {
  data: PropTypes.shape(partialDataShape).isRequired,
};

const UptimeChecks = props => {
  const { data } = props;

  if (!data) return null;

  return (
    <Partial data={data}>
      <InformationsWrapper>
        <PartialValue
          label="Name"
          valuePath="name"
          renderValue={valueOrNone} />

        <PartialValue
          label="Creation Record"
          valuePath="creation_record"
          renderValue={valueOrNone}
        />

        <PartialValue
          label="Mutation Record"
          valuePath="mutation_record"
          renderValue={valueOrNone}
        />

        <PartialValue
          label="Conditions"
          valuePath="conditions"
          renderValue={valueOrNone}
        />

        <PartialValue
          label="Combiner"
          valuePath="combiner"
          renderValue={valueOrNone}
        />

        <PartialValue
          label="Enabled"
          valuePath="enabled"
          renderValue={valueOrNone}
        />
      </InformationsWrapper>
    </Partial>
  );
};

UptimeChecks.propTypes = propTypes;

export default UptimeChecks;
