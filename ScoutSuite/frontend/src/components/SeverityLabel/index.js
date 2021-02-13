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

  if (severity === 'danger') {
    return <div className="severity-label danger">
      <ReportProblemOutlinedIcon fontSize="inherit" /> Insecure
    </div>;
  }

  if (severity === 'warning') {
    return <div className="severity-label warning">
      <ErrorOutlineOutlinedIcon fontSize="inherit" /> Warning
    </div>;
  }

  if (severity === 'success') {
    return <div className="severity-label success">
      <CheckCircleOutlineOutlinedIcon fontSize="inherit" /> Passed
    </div>;
  }

  return <span>Undefined</span>;
  
};

SeverityLabel.propTypes = propTypes;

export default SeverityLabel;
