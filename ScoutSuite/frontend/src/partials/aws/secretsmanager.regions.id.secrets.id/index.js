import React from 'react';
import PropTypes from 'prop-types';

import { 
  partialDataShape, 
  valueOrNone,
  formatDate,
} from '../../../utils/Partials';
import { Partial, PartialValue } from '../../../components/Partial';


const propTypes = {
  data: PropTypes.shape(partialDataShape).isRequired,
};

const Secrets = props => {
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
          label="ARN"
          valuePath="arn"
          renderValue={valueOrNone}
        />
        <PartialValue
          label="Description"
          valuePath="description"
          renderValue={valueOrNone}
        />
        <PartialValue
          label="Last Changed Date"
          valuePath="last_changed_date"
          renderValue={formatDate}
        />
      </div>
    </Partial>
  );
};

Secrets.propTypes = propTypes;

export default Secrets;
