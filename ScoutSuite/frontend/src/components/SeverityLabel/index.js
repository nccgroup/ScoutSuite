import React from 'react';
import { PropTypes } from 'prop-types';
import ReportProblemOutlinedIcon from '@material-ui/icons/ReportProblemOutlined';
import ErrorOutlineOutlinedIcon from '@material-ui/icons/ErrorOutlineOutlined';
import CheckCircleOutlineOutlinedIcon from '@material-ui/icons/CheckCircleOutlineOutlined';

import './style.scss';

const propTypes = {
  severity: PropTypes.string.isRequired,
};

const SeverityLabel = props => {
  const { severity } = props;

  if (severity === 'critical') {
    return <div className="severity-label critical">
      <ReportProblemOutlinedIcon fontSize="inherit" /> Critical
    </div>;
  }

  if (severity === 'danger' || severity === 'high') {
    return <div className="severity-label high">
      <ReportProblemOutlinedIcon fontSize="inherit" /> High
    </div>;
  }

  if (severity === 'warning' || severity === 'medium') {
    return <div className="severity-label medium">
      <ErrorOutlineOutlinedIcon fontSize="inherit" /> Medium
    </div>;
  }

  if (severity === 'low') {
    return <div className="severity-label low">
      <ErrorOutlineOutlinedIcon fontSize="inherit" /> Low
    </div>;
  }

  if (severity === 'info') {
    return <div className="severity-label info">
      <ErrorOutlineOutlinedIcon fontSize="inherit" /> Info
    </div>;
  }

  if (severity === 'success') {
    return <div className="severity-label success">
      <CheckCircleOutlineOutlinedIcon fontSize="inherit" /> All good
    </div>;
  }

  return <span>Undefined</span>;
  
};

SeverityLabel.propTypes = propTypes;

export default SeverityLabel;
