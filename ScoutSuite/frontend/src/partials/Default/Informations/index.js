import React from 'react';
import PropTypes from 'prop-types';
import { isBoolean, isNumber } from 'lodash';

import DetailedValue from '../../../components/DetailedValue';


const propTypes = {
  data: PropTypes.object.isRequired,
};

const Informations = (props) => {
  const { data } = props;

  const informations = Object.entries(data).filter(
    ([, value]) =>
      isNumber(value) || typeof value === 'string' || isBoolean(value),
  );

  return (
    <>
      {informations.map(([key, value]) => (
        <DetailedValue 
          key={key} 
          label={key} 
          value={value}
        />
      ))}
    </>
  );
};

Informations.propTypes = propTypes;

export default Informations;
