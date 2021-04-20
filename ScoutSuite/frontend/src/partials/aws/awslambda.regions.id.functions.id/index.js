import React from 'react';
import PropTypes from 'prop-types';
import get from 'lodash/get';
import isEmpty from 'lodash/isEmpty';

import { partialDataShape } from '../../../utils/Partials';
import { Partial } from '../../../components/Partial';
import { TabsMenu, TabPane } from '../../../components/Partial/PartialTabs';
import InformationsWrapper from '../../../components/InformationsWrapper';
import Informations from './Informations';
import Policy from '../../../components/Partial/Policy';


const propTypes = {
  data: PropTypes.shape(partialDataShape).isRequired,
};

const LambdaFunctions = props => {
  const { data } = props;

  if (!data) return null;

  const policy = get(data, ['item', 'access_policy']);
  const variables = get(data, ['item', 'env_variables']);

  return (
    <Partial data={data}>
      <InformationsWrapper>
        <Informations />
      </InformationsWrapper>

      <TabsMenu>
        <TabPane 
          title="Resource-Based Policy"
          disabled={isEmpty(policy)}
        >
          <Policy policy={policy} />
        </TabPane>
        <TabPane 
          title="Environment Variables"
          disabled={isEmpty(variables)}
        >
          <Policy policy={variables} />
        </TabPane>
      </TabsMenu>
    </Partial>
  );
};

LambdaFunctions.propTypes = propTypes;

export default LambdaFunctions;
