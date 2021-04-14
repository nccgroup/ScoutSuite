import React from 'react';
import PropTypes from 'prop-types';
import sortBy from 'lodash/sortBy';

import ServiceCard from '../../../../components/ServiceCard';
import IssuesCharts from './IssuesCharts';

import './style.scss';


const propTypes = {
  services: PropTypes.arrayOf(PropTypes.object).isRequired,
};

const Summary = (props) => {
  const services = sortBy(props.services, [
    'issues.Critical',
    'issues.High',
    'issues.Medium',
    'issues.Low',
    'issues.Good',
  ]).reverse();

  return (
    <div className="dashboard-summary">
      <div className="overview">
        <h2>Overview</h2>
        <hr />
        <IssuesCharts services={services} />
      </div>

      <div className="services">
        <h2>Services</h2>
        <hr />
        <div className="cards">
          {services.map((service, i) => (
            <ServiceCard {...service} key={i} />
          ))}
        </div>
      </div>
    </div>
  );
};

Summary.propTypes = propTypes;

export default Summary;
