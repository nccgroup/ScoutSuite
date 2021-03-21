
import React from 'react';
import PropTypes from 'prop-types';
import get from 'lodash/get';
import isEmtpy from 'lodash/isEmpty';

import { partialDataShape } from '../../../utils/Partials';
import { 
  Partial, 
  PartialValue,
} from '../../../components/Partial';
import { TabsMenu, TabPane } from '../../../components/Tabs';
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
      <div className="left-pane">
        <h4>Informations</h4>
        <PartialValue
          label="ID"
          valuePath="id"
        />
        <PartialValue
          label="Default"
          valuePath="IsDefault"
          renderValue={value => value.toString()}
        />
      </div>

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
            <ul>
              {subnets.map((net, i) => (
                <li key={i}>
                  {/* TODO: Link to resource */}
                  {net.SubnetId}
                </li>
              ))}
            </ul>
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
