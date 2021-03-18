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
      <h4>Informations</h4>
      {informations.map(([key, value]) => (
        <DetailedValue 
          label={key} 
          value={value}
          renderValue={isBoolean(value) ? value => value.toString() : undefined}
          key={key} 
        />
      ))}
    </>
  );
};

Informations.propTypes = propTypes;

export default Informations;
