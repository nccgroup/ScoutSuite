import React from 'react';
import PropTypes from 'prop-types';
import cx from 'classnames';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faCheckCircle, faExclamationCircle } from '@fortawesome/free-solid-svg-icons';

import './style.scss';

const propTypes = {
  status: PropTypes.oneOf(['issues', 'warnings', 'good']).isRequired,
  amount: PropTypes.number,
};

const defaultProps = {
  amount: 0,
};

const ServiceStatus = props => {
  const { status, amount } = props;

  const classNames = cx('service-status', status);

  const hasIssues = status !== 'good';
  const icon = hasIssues ? faExclamationCircle : faCheckCircle;
  const text = hasIssues ? `${amount} ${status}` : status;

  return (
    <div className={classNames}>
      <FontAwesomeIcon icon={icon} size="sm"/>
      <span>{text}</span>
    </div>
  );
};

ServiceStatus.propTypes = propTypes;
ServiceStatus.defaultProps = defaultProps;

export default ServiceStatus;
