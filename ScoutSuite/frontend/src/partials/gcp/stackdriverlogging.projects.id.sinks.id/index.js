import React from 'react';
import PropTypes from 'prop-types';

import { Partial, PartialValue } from '../../../components/Partial';
import { partialDataShape } from '../../../utils/Partials';

const propTypes = {
  data: PropTypes.shape(partialDataShape).isRequired,
};

const Sinks = props => {
  const { data } = props;

  if (!data) return null;

  return (
    <Partial data={data}>
      <div className="left-pane">
        <PartialValue
          label="Sink Name"
          valuePath="name" />

        <PartialValue
          label="Project ID"
          valuePath="project" />

        <PartialValue
          label="Filter"
          valuePath="filter" />

        <PartialValue
          label="Destination"
          valuePath="destination" />
      </div>
    </Partial>
  );
};

Sinks.propTypes = propTypes;

export default Sinks;
