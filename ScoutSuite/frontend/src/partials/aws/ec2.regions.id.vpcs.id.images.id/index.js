import React from 'react';
import PropTypes from 'prop-types';

import { PartialValue } from '../../../components/Partial';
import { partialDataShape } from '../../../utils/Partials';


const propTypes = {
  data: PropTypes.shape(partialDataShape).isRequired,
};

const Ec2Image = props => {
  const { data } = props;

  if (!data) return null;

  // TODO: test this partial.
  return (
    <div>
      <h4>Informations</h4>
      <PartialValue
        label="ARN"
        valuePath="arn"
      />
      <PartialValue
        label="ID"
        valuePath="id"
      />
      <PartialValue
        label="Architecture"
        valuePath="Architecture"
      />
      <PartialValue
        label="Public"
        valuePath="Public"
      />
    </div>
  );
};

Ec2Image.propTypes = propTypes;

export default Ec2Image;
