import React, { useState } from 'react';
import PropTypes from 'prop-types';

import TabsMenu from '../../components/TabsMenu';
import Summary from './TabsContent/Summary';
import ExecutionDetails from './TabsContent/ExecutionDetails';
import ResourcesDetails from './TabsContent/ResourcesDetails';
import { TAB_NAMES } from '../../utils/Dashboard';

import './style.scss';

const propTypes = {
  services: PropTypes.arrayOf(PropTypes.object).isRequired,
}

const Dashboard = props => {
  const { services } = props;

  const [ selectedTab, setSelectedTab ] = useState(TAB_NAMES.SUMMARY);
  const onClickTab = event => setSelectedTab(event.target.getAttribute('value'))

  const getTabContent = selectedTab => {
    switch (selectedTab) {
      case TAB_NAMES.SUMMARY:
        return <Summary services={services} />;
      case TAB_NAMES.EXECUTION_DETAILS:
        return <ExecutionDetails />;
      case TAB_NAMES.RESOURCES_DETAILS:
        return <ResourcesDetails />;
      default:
        return <div/>;
    }
  }

  return (
    <div className="dashboard">
      <TabsMenu 
        tabs={TAB_NAMES}
        selectedTab={selectedTab}
        onClick={onClickTab}
      />
      {getTabContent(selectedTab)}
    </div>
  );
}

Dashboard.propTypes = propTypes;

export default Dashboard;
