
import React from 'react';
import PropTypes from 'prop-types';

import { partialDataShape, convertBoolToEnable } from '../../../utils/Partials';
import { Partial, PartialValue } from '../../../components/Partial';
import { TabsMenu, TabPane } from '../../../components/Partial/PartialTabs';
import InformationsWrapper from '../../../components/InformationsWrapper';
import Informations from './Informations';


const propTypes = {
  data: PropTypes.shape(partialDataShape).isRequired,
};

const SecurityGroups = props => {
  const { data } = props;

  if (!data) return null;

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
              errorPath="instance_publicly_accessible"
              renderValue={convertBoolToEnable}
            />
          </div>
        </TabPane>
      </TabsMenu> 
    </Partial>
  );
};

SecurityGroups.propTypes = propTypes;

export default SecurityGroups;
