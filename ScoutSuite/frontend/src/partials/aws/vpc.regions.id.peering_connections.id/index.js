
import React from 'react';
import PropTypes from 'prop-types';
import get from 'lodash/get';
import isEmpty from 'lodash/isEmpty';

import { partialDataShape, renderAwsTags } from '../../../utils/Partials';
import { Partial, PartialValue } from '../../../components/Partial';
import { TabsMenu, TabPane } from '../../../components/Partial/PartialTabs';
import InformationsWrapper from '../../../components/InformationsWrapper';
import PeeringConnection from './PeeringConnection';


const propTypes = {
  data: PropTypes.shape(partialDataShape).isRequired,
};

const RegionDomain = props => {
  const { data } = props;

  if (!data) return null;

  const requesterInfos = get(data, ['item', 'RequesterVpcInfo']);
  const accepterInfos = get(data, ['item', 'AccepterVpcInfo']);
  const tags = get(data, ['item', 'Tags'], []);

  return (
    <Partial data={data}>
      <InformationsWrapper>
        <PartialValue 
          label="Status"
          valuePath="Status.Message"
        />
      </InformationsWrapper>

      <TabsMenu>
        <TabPane title="Requester VPC">
          <PeeringConnection connectionInfos={requesterInfos} />
        </TabPane>
        <TabPane title="Accepter VPC">
          <PeeringConnection connectionInfos={accepterInfos} />
        </TabPane>
        {!isEmpty(tags) && (
          <TabPane title="Tags">
            {renderAwsTags(tags)}
          </TabPane>
        )}
      </TabsMenu>
    </Partial>
  );
};

RegionDomain.propTypes = propTypes;

export default RegionDomain;
