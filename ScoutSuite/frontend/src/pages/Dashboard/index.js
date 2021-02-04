import React from 'react';
import PropTypes from 'prop-types';

import ServiceStatus from '../../components/ServiceStatus';
import ServiceCard from '../../components/ServiceCard';

import './style.scss';

const propTypes = {
  services: PropTypes.arrayOf(PropTypes.object).isRequired,
}

const Dashboard = props => {
  const services = props.services.sort((a, b) => b.issues - a.issues || b.warnings - a.warnings);

  console.log(services);

  const issues_sum = services.map(service => service.issues).reduce((total, issues) => total + issues);
  const warnings_sum = services.map(service => service.warnings).reduce((total, warnings) => total + warnings);

  return (
    <div className="dashboard">
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
}

Dashboard.propTypes = propTypes;

export default Dashboard;
