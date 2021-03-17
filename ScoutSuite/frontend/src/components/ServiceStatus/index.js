import React from 'react';
import PropTypes from 'prop-types';
import cx from 'classnames';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import {
  faCheckCircle,
  faExclamationCircle,
} from '@fortawesome/free-solid-svg-icons';
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
  const icon = hasIssues ? faExclamationCircle : faCheckCircle;

  return (
    <Tooltip title={status} placement="top" arrow>
      <div className={classNames}>
        <FontAwesomeIcon icon={icon} size="sm" />
        <span>{amount}</span>
      </div>
    </Tooltip>
  );
};

ServiceStatus.propTypes = propTypes;
ServiceStatus.defaultProps = defaultProps;

export default ServiceStatus;
