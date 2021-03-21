
import React from 'react';
import PropTypes from 'prop-types';
import get from 'lodash/get';
import isEmpty from 'lodash/isEmpty';

import { 
  convertBoolToEnable,
  partialDataShape, 
  valueOrNone 
} from '../../../utils/Partials';
import { 
  Partial, 
  PartialValue,
} from '../../../components/Partial';
import { TabsMenu, TabPane } from '../../../components/Tabs';
import FlowLogs from './FlowLogs';


const propTypes = {
  data: PropTypes.shape(partialDataShape).isRequired,
};

const RegionDomain = props => {
  const { data } = props;

  if (!data) return null;

  const instances = get(data, ['item', 'instances']);
  const flowLogs = get(data, ['item', 'flow_logs']);

  return (
    <Partial data={data}>
      <div className="left-pane">
        <h4>Informations</h4>
        <PartialValue
          label="Name"
          valuePath="name"
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
      </div>

      <TabsMenu>
        {!isEmpty(instances) &&(
          <TabPane title="Instances">
            <ul>
              {instances.map((instance, i) => (
                <li key={i}>
                  {instance.name}
                </li>
              ))}
            </ul>
          </TabPane>
        )}
        <TabPane title="Flow Logs">
          <FlowLogs flowLogs={flowLogs} />
        </TabPane>
      </TabsMenu>
    </Partial>
  );
};

RegionDomain.propTypes = propTypes;

export default RegionDomain;
