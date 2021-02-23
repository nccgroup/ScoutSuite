import React from 'react';
import { PropTypes } from 'prop-types';

import { PartialContext } from '../context';

const propTypes = {
  data: PropTypes.objectOf({
    item: PropTypes.object.isRequired,
    path_to_issues: PropTypes.arrayOf(PropTypes.string).isRequired,
  }).isRequired,
  children: PropTypes.element.isRequired,
};

const PartialWrapper = (props) => {
  const { data, children } = props;

  return (
    <PartialContext.Provider value={data}>
      {children}
    </PartialContext.Provider>
  );
};

PartialWrapper.propTypes = propTypes;

export default PartialWrapper;
