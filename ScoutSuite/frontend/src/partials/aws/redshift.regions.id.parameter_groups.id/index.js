
import React from 'react';
import PropTypes from 'prop-types';
import get from 'lodash/get';

import { partialDataShape } from '../../../utils/Partials';
import { Partial, PartialValue } from '../../../components/Partial';
import { TabsMenu, TabPane } from '../../../components/Partial/PartialTabs';
import InformationsWrapper from '../../../components/InformationsWrapper';

const propTypes = {
  data: PropTypes.shape(partialDataShape).isRequired,
};

const ParameterGroups = props => {
  const { data } = props;

  if (!data) return null;

  const parameters = get(data, ['item', 'parameters']);

  return (
    <Partial data={data}>
      <InformationsWrapper>
        <PartialValue
          label="ARN"
          valuePath="arn"
        />
        <PartialValue
          label="Descripition"
          valuePath="description"
        />
        <PartialValue
          label="Group Family"
          valuePath="family"
        />
        <PartialValue
          label="Default Parameter Group"
          valuePath="is_default"
        />
      </InformationsWrapper>

      <TabsMenu>
        <TabPane title="Parameters">
          <div>
            {Object.entries(parameters).map(([name, parameter], i) => (
              <PartialValue
                key={i}
                label={name}
                value={parameter.value}
                errorPath={name}
              />
            ))}
          </div>
        </TabPane>
      </TabsMenu> 
    </Partial>
  );
};

ParameterGroups.propTypes = propTypes;

export default ParameterGroups;
