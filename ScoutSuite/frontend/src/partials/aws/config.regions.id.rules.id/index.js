import React from 'react';
import PropTypes from 'prop-types';

import { partialDataShape } from '../../../utils/Partials';
import { Partial, PartialValue } from '../../../components/Partial';


const propTypes = {
  data: PropTypes.shape(partialDataShape).isRequired,
};

const ConfigRules = props => {
  const { data } = props;

  if (!data) return null;

  return (
    <Partial data={data}>
      <div>
        <h4>Informations</h4>
        <PartialValue
          label="ID"
          valuePath="id"
        />
        <PartialValue
          label="ARN"
          valuePath="arn"
        />
        <PartialValue
          label="Region"
          valuePath="region"
        />
        <PartialValue
          label="Description"
          valuePath="description"
        />
        <PartialValue
          label="State"
          valuePath="state"
        />
      </div>
    </Partial>
  );
};

ConfigRules.propTypes = propTypes;

export default ConfigRules;
