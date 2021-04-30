import React from 'react';
import PropTypes from 'prop-types';

import { 
  partialDataShape,
  formatDate,
  valueOrNone,
} from '../../../utils/Partials';
import { Partial, PartialValue } from '../../../components/Partial';


const propTypes = {
  data: PropTypes.shape(partialDataShape).isRequired,
};

const MetricFilters = props => {
  const { data } = props;

  if (!data) return null;

  return (
    <Partial data={data}>
      <div>
        <h4>Informations</h4>
        <PartialValue
          label="Name"
          valuePath="name"
          renderValue={valueOrNone}
        />
        <PartialValue
          label="Creation Time"
          valuePath="creation_time"
          renderValue={formatDate}
        />
        <PartialValue
          label="Log Group Name"
          valuePath="log_group_name"
          renderValue={valueOrNone}
        />
        <PartialValue
          label="Pattern"
          valuePath="pattern"
          renderValue={value => (
            <code>{valueOrNone(value)}</code>
          )}
        />
      </div>
    </Partial>
  );
};

MetricFilters.propTypes = propTypes;

export default MetricFilters;
