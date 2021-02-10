import React from 'react';

import Header from './Header';
import Menu from './Menu';
import Dashboard from '../pages/Dashboard';

import './style.scss';

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

const Layout = () => {
  return (
    <div className="main-layout">
      <Header />
      <Menu />
      <div className="main">
        <Dashboard services={services} />
      </div>
    </div>
  );
};

export default Layout;
