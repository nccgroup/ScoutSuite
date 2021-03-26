import React from 'react';
import PropTypes from 'prop-types';
import cx from 'classnames';
import CheckCircleIcon from '@material-ui/icons/CheckCircle';
import ErrorIcon from '@material-ui/icons/Error';
import Tooltip from '@material-ui/core/Tooltip';

import './style.scss';

const propTypes = {
  status: PropTypes.oneOf([
    'critical', 
    'high', 
    'medium', 
    'low', 
    'good',
  ]).isRequired,
  amount: PropTypes.number,
};

const defaultProps = {
  amount: 0,
};

const ServiceStatus = (props) => {
  const { status, amount } = props;

  const classNames = cx('service-status', status);

  const hasIssues = status !== 'good';

  return (
    <Tooltip title={status} placement="top" arrow>
      <div className={classNames}>
        {hasIssues 
          ? <ErrorIcon fontSize="inherit" /> 
          : <CheckCircleIcon fontSize="inherit" />
        }
        <span>{amount}</span>
      </div>
    </Tooltip>
  );
};

ServiceStatus.propTypes = propTypes;
ServiceStatus.defaultProps = defaultProps;

export default ServiceStatus;
