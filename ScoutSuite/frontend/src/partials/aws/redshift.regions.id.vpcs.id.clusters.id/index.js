
import React from 'react';
import PropTypes from 'prop-types';
import get from 'lodash/get';
import isEmtpy from 'lodash/isEmpty';

import { partialDataShape, } from '../../../utils/Partials';
import { Partial, PartialValue } from '../../../components/Partial';
import { TabsMenu, TabPane } from '../../../components/Partial/PartialTabs';
import InformationsWrapper from '../../../components/InformationsWrapper';
import Informations from './Informations';


const propTypes = {
  data: PropTypes.shape(partialDataShape).isRequired,
};

const Clusters = props => {
  const { data } = props;

  if (!data) return null;

  const vpcGroups = get(data, ['item', 'VpcSecurityGroups']);
  const clusterGroups = get(data, ['item', 'ClusterSecurityGroups']);

  return (
    <Partial data={data}>
      <InformationsWrapper>
        <Informations />
      </InformationsWrapper>

      <TabsMenu>
        <TabPane title="Network">
          <div>
            <PartialValue 
              label="Endpoint"
              valuePath="Endpoint"
              renderValue={value => `${value.Address}:${value.Port}`}
            />
            <PartialValue 
              label="Publicly Accessible"
              valuePath="PubliclyAccessible"
            />
            <PartialValue 
              label="VPC"
              valuePath="VpcId"
            />
            <PartialValue 
              label="Subnet"
              valuePath="ClusterSubnetGroupName"
            />
            {!(isEmtpy(vpcGroups) && isEmtpy(clusterGroups)) && (
              <PartialValue
                label="Security Groups"
                renderValue={() => (
                  <>
                    <ul>
                      {vpcGroups.map((group, i) => (
                        <li key={i}>
                          {`${group.VpcSecurityGroupId} ${group.Status}`}
                        </li>
                      ))}
                    </ul>
                    <ul>
                      {clusterGroups.map((group, i) => (
                        <li key={i}>
                          {`${group.ClusterSecurityGroupName} ${group.Status}`}
                        </li>
                      ))}
                    </ul>
                  </>
                )}
              />
            )}
          </div>
        </TabPane>
      </TabsMenu> 
    </Partial>
  );
};

Clusters.propTypes = propTypes;

export default Clusters;
