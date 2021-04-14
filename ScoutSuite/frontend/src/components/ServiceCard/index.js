import React from 'react';
import PropTypes from 'prop-types';
import { Link } from 'react-router-dom';
import ChevronRightIcon from '@material-ui/icons/ChevronRight';
import cx from 'classnames';

import ServiceStatus from '../ServiceStatus';
import DetailedValue from '../DetailedValue';

import './style.scss';


const propTypes = {
  id: PropTypes.string.isRequired,
  name: PropTypes.string.isRequired,
  resources: PropTypes.number.isRequired,
  rules: PropTypes.number.isRequired,
  'flagged-items': PropTypes.number.isRequired,
  issues: PropTypes.object.isRequired,
};

const ServiceCard = props => {
  const { id, name, issues, resources, rules } = props;

  const hasFindings = rules > 0;
  const findingsPath = hasFindings ? `/services/${id}/findings` : '/';

  return (
    <div className="service-card">
      <div className="header">
        <h3>{name}</h3>
        <div className="status">
          {issues.Critical > 0 && (
            <ServiceStatus status="critical" amount={issues.Critical} />
          )}
          {issues.High > 0 && (
            <ServiceStatus status="high" amount={issues.High} />
          )}
          {issues.Medium > 0 && (
            <ServiceStatus status="medium" amount={issues.Medium} />
          )}
          {issues.Low > 0 && <ServiceStatus status="low" amount={issues.Low} />}
          {issues.Good > 0 && (
            <ServiceStatus status="good" amount={issues.Good} />
          )}
        </div>
      </div>
      <hr/>
      <div className="content">
        <DetailedValue
          label="Resources" 
          value={resources}
          separator="" />
        <DetailedValue
          label="Rules" 
          value={rules}
          separator="" />
        <DetailedValue
          label="Flagged Items"
          value={props['flagged-items']}
          separator=""
        />
      </div>
      <hr/>
      <div className="footer">
        <Link
          className={cx('link', { disabled: !hasFindings })}
          to={findingsPath}
        >
          {hasFindings ? (
            <>
              View report <ChevronRightIcon />
            </>
          ) : (
            'No findings'
          )}
        </Link>
      </div>
    </div>
  );
};

ServiceCard.propTypes = propTypes;

export default ServiceCard;
