
import React from 'react';
import PropTypes from 'prop-types';
import get from 'lodash/get';
import isEmpty from 'lodash/isEmpty';

import { 
  partialDataShape,
  convertBoolToEnable,
  valueOrNone,
  renderList,
  renderFlowlogLink,
} from '../../../utils/Partials';
import { 
  Partial, 
  PartialValue,
} from '../../../components/Partial';
import { TabsMenu, TabPane } from '../../../components/Partial/PartialTabs';
import InformationsWrapper from '../../../components/InformationsWrapper';
import ResourceLink from '../../../components/ResourceLink';
import WarningMessage from '../../../components/WarningMessage';


const propTypes = {
  data: PropTypes.shape(partialDataShape).isRequired,
};

const RegionDomain = props => {
  const { data } = props;

  if (!data) return null;

  const id = get(data, ['item', 'id']);
  const instances = get(data, ['item', 'instances'], []);
  const flowLogs = get(data, ['item', 'flow_logs']);

  const renderInstanceLink = id => (
    <ResourceLink 
      service="ec2"
      resource="instances"
      id={id}
    />
  );

  return (
    <Partial data={data}>
      <InformationsWrapper>
        <PartialValue
          label="Name"
          valuePath="name"
          renderValue={
            name => name === id ? 'None' : name
          }
        />
        <PartialValue
          label="ID"
          valuePath="id"
        />
        <PartialValue
          label="VPC ID"
          valuePath="VpcId"
        />
        <PartialValue
          label="Availability Zone"
          valuePath="AvailabilityZone"
        />
        <PartialValue
          label="CIDR Block"
          valuePath="CidrBlock"
        />
        <PartialValue
          label="IPv6 CIDR Block"
          valuePath="CidrBlockv6"
          renderValue={valueOrNone}
        />
        <PartialValue
          label="Public IP on Launch"
          valuePath="MapPublicIpOnLaunch"
          renderValue={convertBoolToEnable}
        />
      </InformationsWrapper>

      <TabsMenu>
        <TabPane 
          title="Instances"
          disabled={isEmpty(instances)}
        >
          {renderList(instances, '', renderInstanceLink)}
        </TabPane>
        <TabPane title="Flow Logs">
          {isEmpty(flowLogs) ? (
            <PartialValue
              errorPath="no_flowlog"
              renderValue={() => (
                <WarningMessage
                  message="This subnet has no flow logs."
                />
              )}
            />
          ) : (
            renderList(
              flowLogs.filter(value => typeof value === 'string'), 
              '',
              renderFlowlogLink,
            )
          )}
        </TabPane>
      </TabsMenu>
    </Partial>
  );
};

RegionDomain.propTypes = propTypes;

export default RegionDomain;
