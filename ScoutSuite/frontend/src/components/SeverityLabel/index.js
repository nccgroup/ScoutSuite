import React from 'react';
import { PropTypes } from 'prop-types';
import ReportProblemOutlinedIcon from '@material-ui/icons/ReportProblemOutlined';
import ErrorOutlineOutlinedIcon from '@material-ui/icons/ErrorOutlineOutlined';
import CheckCircleOutlineOutlinedIcon from '@material-ui/icons/CheckCircleOutlineOutlined';
import cx from 'classnames';

import './style.scss';

const severities = {
  critical: {
    text: 'Critical',
    icon: <ReportProblemOutlinedIcon fontSize="inherit" />
  },
  danger: {
    text: 'High',
    icon: <ReportProblemOutlinedIcon fontSize="inherit" />
  },
  high: {
    text: 'High',
    icon: <ReportProblemOutlinedIcon fontSize="inherit" />
  },
  warning: {
    text: 'Medium',
    icon: <ErrorOutlineOutlinedIcon fontSize="inherit" />
  },
  medium: {
    text: 'Medium',
    icon: <ErrorOutlineOutlinedIcon fontSize="inherit" />
  },
  low: {
    text: 'Low',
    icon: <ErrorOutlineOutlinedIcon fontSize="inherit" />
  },
  info: {
    text: 'Info',
    icon: <ReportProblemOutlinedIcon fontSize="inherit" />
  },
  success: {
    text: 'All good',
    icon: <CheckCircleOutlineOutlinedIcon fontSize="inherit" />
  },
};

const propTypes = {
  severity: PropTypes.string.isRequired,
};

const SeverityLabel = props => {
  const { severity } = props;

  return (
    <div className={cx('severity-label', severity)}>
      {severities[severity].icon} {severities[severity].text}
    </div>
  );
};

SeverityLabel.propTypes = propTypes;

export default SeverityLabel;
