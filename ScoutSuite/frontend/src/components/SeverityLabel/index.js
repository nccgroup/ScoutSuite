import React from 'react';
import PropTypes from 'prop-types';
import cx from 'classnames';

import { SEVERITIES } from '../../utils/Dashboard';

import './style.scss';


const propTypes = {
  severity: PropTypes.string.isRequired,
};

const SeverityLabel = props => {
  const { severity } = props;

  return (
    <div className={cx('severity-label', severity)}>
      {SEVERITIES[severity].icon} {SEVERITIES[severity].text}
    </div>
  );
};

SeverityLabel.propTypes = propTypes;

export default SeverityLabel;
