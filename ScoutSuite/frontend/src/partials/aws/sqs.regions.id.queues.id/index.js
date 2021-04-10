import React from 'react';
import PropTypes from 'prop-types';
import get from 'lodash/get';
import isEmpty from 'lodash/isEmpty';

import { 
  partialDataShape, 
  valueOrNone,
  formatDate,
} from '../../../utils/Partials';
import { Partial, PartialValue } from '../../../components/Partial';
import { TabsMenu, TabPane } from '../../../components/Partial/PartialTabs';
import InformationsWrapper from '../../../components/InformationsWrapper';
import Policy from '../../../components/Partial/Policy';


const propTypes = {
  data: PropTypes.shape(partialDataShape).isRequired,
};

const Queues = props => {
  const { data } = props;

  if (!data) return null;

  const policy = get(data, ['item', 'Policy']);

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
          label="KMS Master Key ID"
          valuePath="kms_master_key_id"
          errorPath="server-side-encryption-disabled"
          renderValue={valueOrNone}
        />
        <PartialValue
          label="Creation Time"
          valuePath="CreatedTimestamp"
          renderValue={value => formatDate(parseInt(value))}
        />
      </InformationsWrapper>

      <TabsMenu>
        <TabPane 
          title="Access Control Policy"
          disabled={isEmpty(policy.Statement)}
        >
          <Policy 
            policy={policy}
            policyPath="Policy"
          />
        </TabPane>
      </TabsMenu>
    </Partial>
  );
};

Queues.propTypes = propTypes;

export default Queues;
