import React from 'react';
import { Router } from '@reach/router';

import Findings from './pages/Findings';
import Resources from './pages/Resources';
import Dashboard from './pages/Dashboard';
import ExternalAttack from './pages/ExternalAttack/index';

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

function App() {
  return (
    <Router>
      <Dashboard path="/" services={services} />
      <Findings path="/services/:service/findings" /> 
      <ExternalAttack path="/services/:service/external-attacks" /> 
      <Resources path="/services/:service/findings/:finding/items" />
      <Resources path="/services/:service/findings/:finding/items/:item" />
      <Resources path="/services/:service/:resources" /> 
    </Router>
  );
}

export default App;
