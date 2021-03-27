
import React from 'react';
import PropTypes from 'prop-types';
import get from 'lodash/get';
import isEmpty from 'lodash/isEmpty';

import {
  partialDataShape,
  renderResourcesAsList,
} from '../../../utils/Partials';
import { Partial } from '../../../components/Partial';
import { TabsMenu, TabPane } from '../../../components/Partial/PartialTabs';
import Informations from './Informations';


const propTypes = {
  data: PropTypes.shape(partialDataShape).isRequired,
};

const RegionDomain = props => {
  const { data } = props;

  if (!data) return null;

  const networkAcls = get(data, ['item', 'network_acls'], {});
  const instances = get(data, ['item', 'instances'], {});
  const flowLogs = get(data, ['item', 'flow_logs'], []);
  const peeringConnections = get(data, ['item', 'peering_connections'], []);


  return (
    <Partial data={data}>
      <div className="left-pane">
        <Informations />
      </div>

      <TabsMenu>
        <TabPane
          title="Network ACLs"
          disabled={isEmpty(networkAcls)}
        >
          {renderResourcesAsList(Object.keys(networkAcls))}
        </TabPane>
        <TabPane
          title="Instances"
          disabled={isEmpty(instances)}
        >
          {renderResourcesAsList(Object.keys(instances))}
        </TabPane>
        <TabPane
          title="Flow Logs"
          disabled={isEmpty(flowLogs)}
        >
          {renderResourcesAsList(flowLogs)}
        </TabPane>
        <TabPane
          title="Peering Connections"
          disabled={isEmpty(peeringConnections)}
        >
          {/* TODO: Add status and id */}
          {renderResourcesAsList(peeringConnections)}
        </TabPane>
        
      </TabsMenu>
    </Partial>
  );
};

RegionDomain.propTypes = propTypes;

export default RegionDomain;
