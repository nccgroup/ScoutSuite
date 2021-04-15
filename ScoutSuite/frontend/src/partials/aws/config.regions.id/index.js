import React from 'react';
import PropTypes from 'prop-types';
import get from 'lodash/get';
import isEmpty from 'lodash/isEmpty';

import { 
  partialDataShape,
  renderList,
} from '../../../utils/Partials';
import { Partial, PartialValue } from '../../../components/Partial';
import { TabsMenu, TabPane } from '../../../components/Partial/PartialTabs';
import InformationsWrapper from '../../../components/InformationsWrapper';
import ResourceLink from '../../../components/ResourceLink';


const propTypes = {
  data: PropTypes.shape(partialDataShape).isRequired,
};

const ConfigRecorders = props => {
  const { data } = props;

  if (!data) return null;

  const recorders = get(data, ['item', 'recorders'], {});
  const rules = get(data, ['item', 'rules'], {});

  const renderRecorderLink = ([id, { name }]) => (
    <ResourceLink 
      service="config"
      resource="recorders"
      id={id}
      name={name}
    />
  );

  const renderRuleLink = ([id, { name }]) => (
    <ResourceLink 
      service="config"
      resource="rules"
      id={id}
      name={name}
    />
  );

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
          {renderList(Object.entries(recorders), '', renderRecorderLink)}
        </TabPane>
        <TabPane
          title="Rules"
          disabled={isEmpty(rules)}
        >
          {renderList(Object.entries(rules), '', renderRuleLink)}
        </TabPane>
      </TabsMenu>
    </Partial>
  );
};

ConfigRecorders.propTypes = propTypes;

export default ConfigRecorders;
