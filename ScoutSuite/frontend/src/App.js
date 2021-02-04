import React from 'react';
import './App.css';

import Dashboard from './pages/Dashboard';

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
]

function App() {
  return (
    <Dashboard services={services} />
  );
}

export default App;
