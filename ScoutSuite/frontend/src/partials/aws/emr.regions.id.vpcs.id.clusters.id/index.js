import React from 'react';
import PropTypes from 'prop-types';
import get from 'lodash/get';
import isEmpty from 'lodash/isEmpty';

import { partialDataShape, valueOrNone } from '../../../utils/Partials';
import { useAPI } from '../../../api/useAPI';
import { getRawEndpoint } from '../../../api/paths';
import { getRegionFromPath, getVpcFromPath } from '../../../utils/Api';
import { Partial, PartialValue } from '../../../components/Partial';
import { TabsMenu, TabPane } from '../../../components/Partial/PartialTabs';
import ResourceLink from '../../../components/ResourceLink';
import InformationsWrapper from '../../../components/InformationsWrapper';
import Informations from './Informations';


const propTypes = {
  data: PropTypes.shape(partialDataShape).isRequired,
};

const Clusters = props => {
  const { data } = props;

  const path = get(data, ['item', 'path'], '');
  const region = getRegionFromPath(path);
  const vpcId = getVpcFromPath(path);

  const { data: vpc, loading } = useAPI(
    getRawEndpoint(`services.ec2.regions.${region}.vpcs.${vpcId}`)
  );

  if (!data || loading) return null;

  if (!isEmpty(vpc)) {
    data.item.vpc = `${vpc.name} (${vpcId})`;
    data.item.region = region;
  }

  const attributes = get(data, ['item', 'Ec2InstanceAttributes']);

  const renderGroupLink = (id, name) => (
    <ResourceLink 
      service="ec2"
      resource="security_groups"
      id={id}
      name={name}
    />
  );

  return (
    <Partial data={data}>
      <InformationsWrapper>
        <Informations />
      </InformationsWrapper>

      <TabsMenu>
        <TabPane title="Master">
          <div>
            <PartialValue 
              label="Public DNS"
              valuePath="MasterPublicDnsName"
              renderValue={valueOrNone}
            />
            <PartialValue 
              label="Security Group"
              value={get(
                vpc,
                ['security_groups', attributes.EmrManagedMasterSecurityGroup, 'name']
              )}
              renderValue={value => (
                renderGroupLink(
                  attributes.EmrManagedMasterSecurityGroup,
                  value,
                )
              )}
            />
          </div>
        </TabPane>
        <TabPane 
          title="Slave"
          disabled={isEmpty(attributes.EmrManagedSlaveSecurityGroup)}
        >
          <PartialValue 
            label="Security Group"
            value={get(
              vpc,
              ['security_groups', attributes.EmrManagedSlaveSecurityGroup, 'name']
            )}
            renderValue={value => (
              renderGroupLink(
                attributes.EmrManagedSlaveSecurityGroup,
                value,
              )
            )}
          />
        </TabPane>
      </TabsMenu>
    </Partial>
  );
};

Clusters.propTypes = propTypes;

export default Clusters;
