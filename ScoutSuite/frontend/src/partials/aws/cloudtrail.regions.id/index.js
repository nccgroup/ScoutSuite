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

const Trails = props => {
  const { data } = props;

  if (!data) return null;

  const trails = get(data, ['item', 'trails'], []);

  return (
    <Partial data={data}>
      <InformationsWrapper>
        <PartialValue 
          label="Configured"
          valuePath="trails_count"
          errorPath="NotConfigured"
          renderValue={value => Boolean(value).toString()}
        />
      </InformationsWrapper>

      <TabsMenu>
        <TabPane
          title="Trails"
          disabled={isEmpty(trails)}
        >
          {renderResourcesAsList(Object.values(trails), 'name')}
        </TabPane>
      </TabsMenu>
    </Partial>
  );
};

Trails.propTypes = propTypes;

export default Trails;
