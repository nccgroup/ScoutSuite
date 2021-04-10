import React from 'react';
import PropTypes from 'prop-types';
import get from 'lodash/get';
import isEmpty from 'lodash/isEmpty';

import { 
  partialDataShape, 
  renderResourcesAsList 
} from '../../../utils/Partials';
import { Partial } from '../../../components/Partial';
import { TabsMenu, TabPane } from '../../../components/Partial/PartialTabs';
import InformationsWrapper from '../../../components/InformationsWrapper';
import Informations from './Informations';
import Policy from '../../../components/Partial/Policy';


const propTypes = {
  data: PropTypes.shape(partialDataShape).isRequired,
};

const CloudtrailStack = props => {
  const { data } = props;

  if (!data) return null;

  const capabilities = get(data, ['item', 'Capabilities'], []);
  const policy = get(data, ['item', 'policy']);

  return (
    <Partial data={data}>
      <InformationsWrapper>
        <Informations />
      </InformationsWrapper>

      <TabsMenu>
        <TabPane
          title="Capabilities"
          disabled={isEmpty(capabilities)}
        >
          {renderResourcesAsList(capabilities)}
        </TabPane>
        <TabPane
          title="Stack Policy"
          disabled={isEmpty(policy)}
        >
          <Policy policy={policy} />
        </TabPane>
      </TabsMenu>
    </Partial>
  );
};

CloudtrailStack.propTypes = propTypes;

export default CloudtrailStack;
