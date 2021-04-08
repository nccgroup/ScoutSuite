import React from 'react';
import PropTypes from 'prop-types';
import cx from 'classnames';
import ReportProblemOutlinedIcon from '@material-ui/icons/ReportProblemOutlined';

import './style.scss';


const propTypes = {
  message: PropTypes.string.isRequired,
  icon: PropTypes.element,
  className: PropTypes.string,
};

const defaultProps = {
  icon: <ReportProblemOutlinedIcon fontSize="inherit" />
};

const WarningMessage = props => {
  const { 
    message, 
    icon,
    className,
  } = props;

  return (
    <div className={cx('warning-message', className)}>
      {icon}
      {message}
    </div>
  );
};

WarningMessage.propTypes = propTypes;
WarningMessage.defaultProps = defaultProps;

export default WarningMessage;
