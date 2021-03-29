
import React from 'react';
import PropTypes from 'prop-types';
import get from 'lodash/get';
import isEmpty from 'lodash/isEmpty';

import { partialDataShape } from '../../../utils/Partials';
import { Partial } from '../../../components/Partial';
import { TabsMenu, TabPane } from '../../../components/Partial/PartialTabs';
import InformationsWrapper from '../../../components/InformationsWrapper';
import Informations from './Informations';
import DetailedValue from '../../../components/DetailedValue';


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
        <TabPane 
          title="Tags"
          disabled={isEmpty(tags)}
        >
          <ul>
            {tags.map((tag, i) => (
              <li key={i}>
                <DetailedValue
                  label={tag.Key}
                  value={tag.Value}
                />
              </li>
            ))}
          </ul>
        </TabPane>
      </TabsMenu>
    </Partial>
  );
};

RegionDomain.propTypes = propTypes;

export default RegionDomain;
