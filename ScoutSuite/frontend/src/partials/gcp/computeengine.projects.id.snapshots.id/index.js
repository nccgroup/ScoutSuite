import React from 'react';
import PropTypes from 'prop-types';

import { Partial, PartialValue } from '../../../components/Partial';
import { partialDataShape, formatDate } from '../../../utils/Partials';
import InformationsWrapper from '../../../components/InformationsWrapper';

const propTypes = {
  data: PropTypes.shape(partialDataShape).isRequired,
};

const Snapshots = props => {
  const { data } = props;

  if (!data) return null;

  return (
    <Partial data={data}>
      <InformationsWrapper>
        <PartialValue
          label="Name"
          valuePath="name" />

        <PartialValue
          label="Project ID"
          valuePath="project" />

        <PartialValue
          label="Description"
          valuePath="description" />

        <PartialValue
          label="Creation Date"
          valuePath="creation_timestamp"
          renderValue={formatDate}
        />

        <PartialValue
          label="Status"
          valuePath="status" />
      </InformationsWrapper>
    </Partial>
  );
};

Snapshots.propTypes = propTypes;

export default Snapshots;
