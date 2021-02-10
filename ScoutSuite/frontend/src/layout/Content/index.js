import { Router } from '@reach/router';
import Dashboard from '../../pages/Dashboard/';
import React from 'react';

import './style.scss';
import Findings from '../../pages/Findings/index';
import Resources from '../../pages/Resources';


// TODO: Change for API hook
const services = [
  {
    name: 'EC2',
    warnings: 6,
    issues: 6,
    resources: 1450,
    rules: 607,
    checks: 439,
  },
  {
    name: 'IAM',
    warnings: 0,
    issues: 0,
    resources: 0,
    rules: 0,
    checks: 0,
  },
  {
    name: 'S3',
    warnings: 17,
    issues: 15,
    resources: 3514,
    rules: 1097,
    checks: 786,
  },
];

const Content = () => {
  return (
    <div>
      <Router>
        <Dashboard path="/" services={services} />
        <Findings path="/services/:service/findings" /> 
        <Resources path="/services/:service/findings/:finding/items" />
        <Resources path="/services/:service/findings/:finding/items/:item" />
        <Resources path="/services/:service/:resources" /> 
      </Router>
    </div>
  );
};

export default Content;
