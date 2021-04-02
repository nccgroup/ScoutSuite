
import React from 'react';
import PropTypes from 'prop-types';
import get from 'lodash/get';
import isEmpty from 'lodash/isEmpty';

import { partialDataShape, renderTags } from '../../../utils/Partials';
import { Partial } from '../../../components/Partial';
import { TabsMenu, TabPane } from '../../../components/Partial/PartialTabs';
import InformationsWrapper from '../../../components/InformationsWrapper';
import Informations from './Informations';


const propTypes = {
  data: PropTypes.shape(partialDataShape).isRequired,
};

const RegionDomain = props => {
  const { data } = props;

  if (!data) return null;

  const tags = get(data, ['item', 'tags'], []);

  return (
    <Partial data={data}>
      <InformationsWrapper>
        <Informations />
      </InformationsWrapper>

      <TabsMenu>
        {!isEmpty(tags) && (
          <TabPane title="Tags">
            {renderTags(tags)}
          </TabPane>
        )}
      </TabsMenu>
    </Partial>
  );
};

RegionDomain.propTypes = propTypes;

export default RegionDomain;
