import React from 'react';
import PropTypes from 'prop-types';

import { TabsMenu, TabPane } from '../../components/Tabs/';
import Summary from './TabsContent/Summary';
import ExecutionDetails from './TabsContent/ExecutionDetails';
import ResourcesDetails from './TabsContent/ResourcesDetails';
import { TAB_NAMES } from '../../utils/Dashboard';

import './style.scss';
import Layout from '../../layout/index';

const propTypes = {
  services: PropTypes.arrayOf(PropTypes.object).isRequired,
};

const Dashboard = props => {
  const { services } = props;

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
