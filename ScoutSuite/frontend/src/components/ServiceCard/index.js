import React from 'react';
import PropTypes from 'prop-types';
import { Link } from '@reach/router';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faChevronRight } from '@fortawesome/free-solid-svg-icons';

import ServiceStatus from '../ServiceStatus';
import DetailedValue from '../DetailedValue';

import './style.scss';

const propTypes = {
  name: PropTypes.string.isRequired,
  warnings: PropTypes.number.isRequired,
  issues: PropTypes.number.isRequired,
  resources: PropTypes.number.isRequired,
  rules: PropTypes.number.isRequired,
  checks: PropTypes.number.isRequired,
}

const ServiceCard = props => {
  const {
    name,
    warnings,
    issues,
    resources,
    rules,
    checks,
  } = props;
  
  return (
    <div className="service-card">
      <div className="header">
        <h3>{name}</h3>
        <div className="status">
          {!issues && !warnings && (
            <ServiceStatus status="good"/>
          )}
          {issues > 0 && (
            <ServiceStatus status="issues" amount={issues}/>
          )}
          {warnings > 0 && (
            <ServiceStatus status="warnings" amount={warnings}/>
          )}
        </div>
      </div>
      <hr/>
      <div className="content">
        <DetailedValue label="Resources" value={resources} />
        <DetailedValue label="Rules" value={rules} />
        <DetailedValue label="Checks" value={checks} />
      </div>
      <hr/>
      <div className="footer">
        <Link className="link" to="report/TEMP">
          View report <FontAwesomeIcon icon={faChevronRight}/>
        </Link>
      </div>
    </div>
  );
}

ServiceCard.propTypes = propTypes;

export default ServiceCard;
