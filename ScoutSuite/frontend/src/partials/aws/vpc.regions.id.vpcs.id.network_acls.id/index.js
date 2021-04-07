
import React from 'react';
import PropTypes from 'prop-types';
import get from 'lodash/get';
import isEmtpy from 'lodash/isEmpty';

import { 
  partialDataShape,
  renderResourcesAsList,
} from '../../../utils/Partials';
import { 
  Partial, 
  PartialValue,
} from '../../../components/Partial';
import { TabsMenu, TabPane } from '../../../components/Partial/PartialTabs';
import InformationsWrapper from '../../../components/InformationsWrapper';
import RulesTable from './RulesTable';
import WarningMessage from '../../../components/WarningMessage';


const propTypes = {
  data: PropTypes.shape(partialDataShape).isRequired,
};

const RegionDomain = props => {
  const { data } = props;

  if (!data) return null;

  const rules = get(data, ['item', 'rules']);
  const subnets = get(data, ['item', 'Associations']);

  return (
    <Partial data={data}>
      <InformationsWrapper>
        <PartialValue
          label="ID"
          valuePath="id"
        />
        <PartialValue
          label="Default"
          valuePath="IsDefault"
        />
      </InformationsWrapper>

      <TabsMenu>
        <TabPane title="Egress Rules">
          <RulesTable 
            rules={rules}
            type="egress"
          />
        </TabPane>
        <TabPane title="Ingress Rules">
          <RulesTable 
            rules={rules}
            type="ingress"
          />
        </TabPane>
        <TabPane title="Associated Subnets">
          {!isEmtpy(subnets) ? (
            renderResourcesAsList(subnets, 'SubnetId')
          ) : (
            <PartialValue 
              valuePath="IsDefault"
              errorPath="unused"
              renderValue={value => (
                !value && (
                  <WarningMessage 
                    message="This network ACL is not the VPC's default NACL and is not associated with any existing VPC."
                  />
                )
              )}
            />
          )}
        </TabPane>
      </TabsMenu>
    </Partial>
  );
};

RegionDomain.propTypes = propTypes;

export default RegionDomain;
