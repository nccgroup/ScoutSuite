import React from 'react';

import { TabsMenu, TabPane } from '../../components/Tabs/';
import Layout from '../../layout/index';
import Summary from './TabsContent/Summary';
import ExecutionDetails from './TabsContent/ExecutionDetails';
import ResourcesDetails from './TabsContent/ResourcesDetails';
import { useAPI } from '../../api/useAPI';
import { TAB_NAMES } from '../../utils/Dashboard';

import './style.scss';



const Dashboard = () => {
  const { data: services, loading } = useAPI('raw/last_run/summary');

  if (loading) return null;

  const serivcesList = Object.entries(services).map(([name, item]) => ({name, ...item}));

  return (
    <Layout>
      <div className="dashboard">
        <TabsMenu>
          <TabPane title={TAB_NAMES.SUMMARY}>
            <Summary services={serivcesList} />
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

export default Dashboard;
