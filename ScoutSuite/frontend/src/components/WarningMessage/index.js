import React from 'react';
import PropTypes from 'prop-types';
import ReportProblemOutlinedIcon from '@material-ui/icons/ReportProblemOutlined';

import './style.scss';


const propTypes = {
  message: PropTypes.string.isRequired,
  icon: PropTypes.element,
};

const defaultProps = {
  icon: <ReportProblemOutlinedIcon fontSize="inherit" />
};

const WarningMessage = props => {
  const { message, icon } = props;

  return (
    <div className="warning-message">
      {icon}
      {message}
    </div>
  );
};

WarningMessage.propTypes = propTypes;
WarningMessage.defaultProps = defaultProps;

export default WarningMessage;
