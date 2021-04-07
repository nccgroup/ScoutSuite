import React from 'react';
import PropTypes from 'prop-types';
import get from 'lodash/get';
import isEmpty from 'lodash/isEmpty';

import { 
  partialDataShape,
  renderResourcesAsList,
} from '../../../utils/Partials';
import { Partial, PartialValue } from '../../../components/Partial';
import { TabsMenu, TabPane } from '../../../components/Partial/PartialTabs';
import InformationsWrapper from '../../../components/InformationsWrapper';


const propTypes = {
  data: PropTypes.shape(partialDataShape).isRequired,
};

const ConfigRecorders = props => {
  const { data } = props;

  if (!data) return null;

  const recorders = get(data, ['item', 'recorders'], {});
  const rules = get(data, ['item', 'rules'], {});

  return (
    <Partial data={data}>
      <InformationsWrapper>
        <PartialValue
          label="AWS Config Recorder enabled"
          valuePath="recorders_count"
          errorPath="NotConfigured"
          renderValue={value => Boolean(value).toString()}
        />
      </InformationsWrapper>
      <TabsMenu>
        <TabPane
          title="Recorders"
          disabled={isEmpty(recorders)}
        >
          {renderResourcesAsList(Object.keys(recorders))}
        </TabPane>
        <TabPane
          title="Rules"
          disabled={isEmpty(rules)}
        >
          {renderResourcesAsList(Object.keys(rules))}
        </TabPane>
      </TabsMenu>
    </Partial>
  );
};

ConfigRecorders.propTypes = propTypes;

export default ConfigRecorders;
