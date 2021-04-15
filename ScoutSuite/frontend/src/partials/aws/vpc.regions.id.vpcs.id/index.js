
import React from 'react';
import PropTypes from 'prop-types';
import get from 'lodash/get';
import isEmpty from 'lodash/isEmpty';

import {
  partialDataShape,
  renderList,
  renderResourceLink,
  renderFlowlogLink,
} from '../../../utils/Partials';
import { Partial } from '../../../components/Partial';
import { TabsMenu, TabPane } from '../../../components/Partial/PartialTabs';
import InformationsWrapper from '../../../components/InformationsWrapper';
import Informations from './Informations';
import ResourceLink from '../../../components/ResourceLink';


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

  const renderPeeringLink = id => (
    <ResourceLink
      service="vpc"
      resource="peering_connections"
      id={id}
      nameProps={{
        renderData: data => 
          `${data.name} (${data.Status.Message}, ${data.peer_info.name})`
      }}
    />
  );

  return (
    <Partial data={data}>
      <InformationsWrapper>
        <Informations />
      </InformationsWrapper>

      <TabsMenu>
        <TabPane
          title="Network ACLs"
          disabled={isEmpty(networkAcls)}
        >
          {renderList(Object.values(networkAcls), '', renderResourceLink('vpc', 'network_acls'))}
        </TabPane>
        <TabPane
          title="Instances"
          disabled={isEmpty(instances)}
        >
          {/* TODO: confirm validity of instances tab */}
          {renderList(Object.keys(instances))}
        </TabPane>
        <TabPane
          title="Flow Logs"
          disabled={isEmpty(flowLogs)}
        >
          <div>
            {renderList(flowLogs, '', renderFlowlogLink)}
          </div>
        </TabPane>
        <TabPane
          title="Peering Connections"
          disabled={isEmpty(peeringConnections)}
        >
          {renderList(peeringConnections, '', renderPeeringLink)}
        </TabPane>
        
      </TabsMenu>
    </Partial>
  );
};

RegionDomain.propTypes = propTypes;

export default RegionDomain;
