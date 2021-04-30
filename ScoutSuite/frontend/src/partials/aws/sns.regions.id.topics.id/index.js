import React from 'react';
import PropTypes from 'prop-types';
import get from 'lodash/get';
import isEmpty from 'lodash/isEmpty';

import { partialDataShape,  } from '../../../utils/Partials';
import { Partial, PartialValue } from '../../../components/Partial';
import { TabsMenu, TabPane } from '../../../components/Partial/PartialTabs';
import InformationsWrapper from '../../../components/InformationsWrapper';
import Policy from '../../../components/Partial/Policy';


const propTypes = {
  data: PropTypes.shape(partialDataShape).isRequired,
};

const Topics = props => {
  const { data } = props;

  if (!data) return null;

  const controlPolicy = get(data, ['item', 'Policy']);
  const deliveryPolicy = get(data, ['item', 'DeliveryPolicy']);
  const effectiveDeliveryPolicy = get(data, ['item', 'EffectiveDeliveryPolicy']);
  const subscriptions = get(data, ['item', 'subscriptions']);

  return (
    <Partial data={data}>
      <InformationsWrapper>
        <PartialValue
          label="Region"
          valuePath="region"
        />
        <PartialValue
          label="ARN"
          valuePath="arn"
        />
        <PartialValue
          label="Display Name"
          valuePath="DisplayName"
        />
      </InformationsWrapper>

      <TabsMenu>
        <TabPane 
          title="Access Control Policy"
          disabled={isEmpty(controlPolicy)}
        >
          <Policy 
            policy={controlPolicy}
            policyPath="Policy"
          />
        </TabPane>
        <TabPane 
          title="Delivery Policy"
          disabled={isEmpty(deliveryPolicy)}
        >
          <Policy 
            policy={deliveryPolicy}
            policyPath="DeliveryPolicy"
          />
        </TabPane>
        <TabPane 
          title="Effective Delivery Policy"
          disabled={isEmpty(effectiveDeliveryPolicy)}
        >
          <Policy 
            policy={effectiveDeliveryPolicy}
            policyPath="EffectiveDeliveryPolicy"
          />
        </TabPane>
        <TabPane 
          title="Subscriptions"
          disabled={isEmpty(subscriptions.protocol)}
        >
          <ul>
            {Object.entries(subscriptions.protocol).map(([name, topics], i) => (
              <div key={i}>
                <li>{name}</li>
                <ul>
                  {topics.map((topic, i) => (
                    <li key={i}>
                      {`Endpoint: ${topic.Endpoint}`}
                    </li>
                  ))}
                </ul>
              </div>
            ))}
          </ul>
        </TabPane>
      </TabsMenu>
    </Partial>
  );
};

Topics.propTypes = propTypes;

export default Topics;
