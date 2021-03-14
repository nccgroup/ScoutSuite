import React from 'react';
import PropTypes from 'prop-types';

import SeverityLabel from '../../../../components/SeverityLabel';

const propTypes = {
  value: PropTypes.string.isRequired
};

const Severity = props => {
  const { value } = props;

  return (
    <SeverityLabel severity={value} />
  );
};

Severity.propTypes = propTypes;

export default Severity;
