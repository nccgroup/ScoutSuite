import React from 'react';
import PropTypes from 'prop-types';

import { PartialContext } from '../context';
import { partialDataShape } from '../../../utils/Partials';

const propTypes = {
  data: PropTypes.shape(partialDataShape).isRequired,
  children: PropTypes.oneOfType([
    PropTypes.element,
    PropTypes.arrayOf(PropTypes.element),
  ]).isRequired,
};

const PartialWrapper = (props) => {
  const { data, children } = props;

  console.info('PARTIAL DATA', data);

  return (
    <PartialContext.Provider value={data}>
      {children}
    </PartialContext.Provider>
  );
};

PartialWrapper.propTypes = propTypes;

export default PartialWrapper;
