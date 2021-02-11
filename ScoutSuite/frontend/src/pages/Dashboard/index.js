import React from 'react';
import PropTypes from 'prop-types';

import { TabsMenu, TabPane } from '../../components/Tabs/';
import Layout from '../../layout/index';
import Summary from './TabsContent/Summary';
import ExecutionDetails from './TabsContent/ExecutionDetails';
import ResourcesDetails from './TabsContent/ResourcesDetails';
import { TAB_NAMES } from '../../utils/Dashboard';

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

const Dashboard = () => {
  return (
    <Layout>
      <div className="dashboard">
        <TabsMenu>
          <TabPane title={TAB_NAMES.SUMMARY}>
            <Summary services={services} />
          </TabPane>
          <TabPane title={TAB_NAMES.EXECUTION_DETAILS}>
            <ExecutionDetails />
          </TabPane>
          <TabPane title={TAB_NAMES.RESOURCES_DETAILS}>
            <ResourcesDetails />
          </TabPane>
        </TabsMenu>
      </div>
    </Layout>
  );
};

Dashboard.propTypes = propTypes;

export default Dashboard;
