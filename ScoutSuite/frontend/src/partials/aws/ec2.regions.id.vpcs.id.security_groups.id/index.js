import React from 'react';
import PropTypes from 'prop-types';
import get from 'lodash/get';
import isEmpty from 'lodash/isEmpty';

import { useAPI } from '../../../api/useAPI';
import { getVpcFromPath, getRegionFromPath } from '../../../utils/Api';
import { getRawEndpoint } from '../../../api/paths';
import { Partial, PartialSection } from '../../../components/Partial';
import { partialDataShape } from '../../../utils/Partials';
import { TabsMenu, TabPane } from '../../../components/Partial/PartialTabs';
import InformationsWrapper from '../../../components/InformationsWrapper';
import Informations from './Informations';
import RulesList from './RulesList';
import Usage from './Usage';


const propTypes = {
  data: PropTypes.shape(partialDataShape).isRequired,
};

const Ec2SecurityGroups = props => {
  const { data } = props;

  const path = get(data, ['item', 'path'], '');
  const region = getRegionFromPath(path);
  const vpcId = getVpcFromPath(path);

  const { data: vpc, loading } = useAPI(
    getRawEndpoint(`services.ec2.regions.${region}.vpcs.${vpcId}.name`)
  );

  if (!data || loading) return null;

  if (!isEmpty(vpc)) {
    data.item.vpc = `${vpc} (${vpcId})`;
    data.item.region = region;
  }

  return (
    <Partial data={data}>
      <InformationsWrapper>
        <Informations />
      </InformationsWrapper>

      <TabsMenu>
        <TabPane title="Egress Rules">
          <PartialSection path="rules.egress">
            <RulesList />
          </PartialSection>
        </TabPane>
        <TabPane title="Ingress Rules">
          <PartialSection path="rules.ingress">
            <RulesList />
          </PartialSection>
        </TabPane>
        <TabPane title="Usage">
          <PartialSection path="used_by">
            <Usage />
          </PartialSection>
        </TabPane>
      </TabsMenu>
    </Partial>
  );
};

Ec2SecurityGroups.propTypes = propTypes;

export default Ec2SecurityGroups;
