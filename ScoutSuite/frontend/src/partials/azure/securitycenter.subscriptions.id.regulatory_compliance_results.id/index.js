import React from 'react';
import PropTypes from 'prop-types';

import InformationsWrapper from '../../../components/InformationsWrapper';
import { Partial, PartialValue } from '../../../components/Partial';
import { partialDataShape, valueOrNone } from '../../../utils/Partials';

const propTypes = {
  data: PropTypes.shape(partialDataShape).isRequired,
};

const RegulatoryComplianceResults = props => {
  const { data } = props;

  if (!data) return null;

  return (
    <Partial data={data}>
      <InformationsWrapper>
        <PartialValue
          label="Standard"
          valuePath="standard_name"
          renderValue={valueOrNone}
        />

        <PartialValue
          label="Reference"
          valuePath="reference"
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
          label="Passed Assessments"
          valuePath="passed_assessments"
          renderValue={valueOrNone}
        />

        <PartialValue
          label="Failed Assessments"
          valuePath="failed_assessments"
          renderValue={valueOrNone}
        />

        <PartialValue
          label="Skipped Assessments"
          valuePath="skipped_assessments"
          renderValue={valueOrNone}
        />
      </InformationsWrapper>
    </Partial>
  );
};

RegulatoryComplianceResults.propTypes = propTypes;

export default RegulatoryComplianceResults;
