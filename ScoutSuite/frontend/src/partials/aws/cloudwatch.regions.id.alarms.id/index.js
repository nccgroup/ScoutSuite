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
import Informations from './Informations';
import WarningMessage from '../../../components/WarningMessage';


const propTypes = {
  data: PropTypes.shape(partialDataShape).isRequired,
};

const MetricFilters = props => {
  const { data } = props;

  if (!data) return null;

  const actions = get(data, ['item', 'AlarmActions']);
  const alarms = get(data, ['item', 'InsufficientDataActions'], []);

  return (
    <Partial data={data}>
      <InformationsWrapper>
        <Informations />
      </InformationsWrapper>
      
      <TabsMenu>
        <TabPane title="Alarm Actions">
          {!isEmpty(actions) ? (
            renderResourcesAsList(actions)
          ) : (
            <PartialValue
              errorPath="NoActions"
              renderValue={() => (
                <WarningMessage
                  message="No actions have been configured for this alarm."
                />
              )}
            />
          )}
        </TabPane>
        <TabPane 
          title="Insufficient Data Actions"
          disabled={isEmpty(alarms)}
        >
          {renderResourcesAsList(alarms)}
        </TabPane>
      </TabsMenu>
    </Partial>
  );
};

MetricFilters.propTypes = propTypes;

export default MetricFilters;
