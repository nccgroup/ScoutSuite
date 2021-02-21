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
  resources_count: PropTypes.number.isRequired,
  rules_count: PropTypes.number.isRequired,
  checked_items: PropTypes.number.isRequired,
};

const ServiceCard = props => {
  const {
    name,
    warnings,
    issues,
    resources_count,
    rules_count,
    checked_items,
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
        <DetailedValue label="Resources" value={resources_count} separator="" />
        <DetailedValue label="Rules" value={rules_count} separator="" />
        <DetailedValue label="Checks" value={checked_items} separator="" />
      </div>
      <hr/>
      <div className="footer">
        <Link className="link" to={`/services/${name.toLowerCase()}/findings`}>
          View report <FontAwesomeIcon icon={faChevronRight}/>
        </Link>
      </div>
    </div>
  );
};

ServiceCard.propTypes = propTypes;

export default ServiceCard;
