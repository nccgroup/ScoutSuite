import React from 'react';
import PropTypes from 'prop-types';

import { Partial, PartialValue } from '../../../components/Partial';
import { partialDataShape, valueOrNone } from '../../../utils/Partials';

const propTypes = {
  data: PropTypes.shape(partialDataShape).isRequired,
};

const Metrics = props => {
  const { data } = props;

  if (!data) return null;

  return (
    <Partial data={data}>
      <div className="left-pane">
        <PartialValue
          label="Name"
          valuePath="name" />

        <PartialValue
          label="Project ID"
          valuePath="project" />

        <PartialValue
          label="Description"
          valuePath="description"
          renderValue={valueOrNone}
        />

        <PartialValue
          label="Filter"
          valuePath="filter" />
      </div>
    </Partial>
  );
};

Metrics.propTypes = propTypes;

export default Metrics;
