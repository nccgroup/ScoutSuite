import React from 'react';
import PropTypes from 'prop-types';

import ServiceStatus from '../../../../components/ServiceStatus';
import ServiceCard from '../../../../components/ServiceCard';

import './style.scss';

const propTypes = {
  services: PropTypes.arrayOf(PropTypes.object).isRequired,
};

const Summary = props => {
  const services = props.services.sort((a, b) => b.issues.High - a.issues.High);

  //const issues_sum = services.map(service => service.issues).reduce((total, issues) => total + issues);
  //const warnings_sum = services.map(service => service.warnings).reduce((total, warnings) => total + warnings);
  const issues_sum = 10;
  const warnings_sum = 27;

  return (
    <div className="dashboard-summary">
      <div className="overview"> 
        <h1>Overview</h1>
        <hr/>
        <div className="summary">
          <ServiceStatus status="issues" amount={issues_sum} />
          <ServiceStatus status="warnings" amount={warnings_sum} />
        </div>
      </div>
      
      <div className="services">
        <h1>Services</h1>
        <hr/>
        <div className="cards">
          {services.map((service, i) => (
            <ServiceCard {...service} key={i}/>
          ))}
        </div>
      </div>
    </div>
  );
};

Summary.propTypes = propTypes;

export default Summary;
