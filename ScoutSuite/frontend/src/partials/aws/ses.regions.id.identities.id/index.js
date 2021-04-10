
import React from 'react';
import PropTypes from 'prop-types';
import get from 'lodash/get';
import isEmpty from 'lodash/isEmpty';

import { partialDataShape } from '../../../utils/Partials';
import { Partial, PartialValue } from '../../../components/Partial';
import { TabsMenu, TabPane } from '../../../components/Partial/PartialTabs';
import InformationsWrapper from '../../../components/InformationsWrapper';
import Policy from '../../../components/Partial/Policy';


const propTypes = {
  data: PropTypes.shape(partialDataShape).isRequired,
};

const Identities = props => {
  const { data } = props;

  if (!data) return null;

  const policies = get(data, ['item', 'policies'], {});

  return (
    <Partial data={data}>
      <InformationsWrapper>
        <PartialValue
          label="ARN"
          valuePath="arn"
        />
      </InformationsWrapper>

      <TabsMenu>
        <TabPane title="DKIM Configuration">
          <div>
            <PartialValue
              label="Enabled"
              valuePath="DkimEnabled"
            />
            <PartialValue
              label="Verification Status"
              valuePath="DkimVerificationStatus"
            />
          </div>
        </TabPane>
        <TabPane
          title="Policies"
          disabled={isEmpty(policies)}
        >
          <div>
            {Object.entries(policies).map(([name, policy], i) => (
              <Policy
                key={i}
                name={name}
                policy={policy}
                policyPath={`policies.${name}`}
              />
            ))}
          </div>
        </TabPane>
      </TabsMenu>
    </Partial>
  );
};

Identities.propTypes = propTypes;

export default Identities;
