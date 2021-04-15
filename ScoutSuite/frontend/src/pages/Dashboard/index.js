import React from 'react';

import { TabsMenu, TabPane } from '../../components/Tabs';
import Summary from './TabsContent/Summary';
import ExecutionDetails from './TabsContent/ExecutionDetails';
import ResourcesDetails from './TabsContent/ResourcesDetails';
import { useAPI } from '../../api/useAPI';
import { TAB_NAMES } from '../../utils/Dashboard';
import Breadcrumb from '../../components/Breadcrumb/index';

import './style.scss';
import ErrorBoundary from '../../components/ErrorBoundary/index';

const Dashboard = () => {
  const { data: services, loading } = useAPI('dashboard');

  if (loading) return null;

  const serivcesList = Object.entries(services).map(([name, item]) => ({name, ...item}));

  return (
    <>
      <Breadcrumb />
      <div className="dashboard">
        <TabsMenu>
          <TabPane title={TAB_NAMES.SUMMARY}>
            <ErrorBoundary>
              <Summary services={serivcesList} />
            </ErrorBoundary>
          </TabPane>
          <TabPane title={TAB_NAMES.EXECUTION_DETAILS}>
            <ErrorBoundary>
              <ExecutionDetails />
            </ErrorBoundary>
          </TabPane>
          <TabPane title={TAB_NAMES.RESOURCES_DETAILS}>
            <ErrorBoundary>
              <ResourcesDetails />
            </ErrorBoundary>
          </TabPane>
        </TabsMenu>
      </div>
    </>
  );
};

export default Dashboard;
