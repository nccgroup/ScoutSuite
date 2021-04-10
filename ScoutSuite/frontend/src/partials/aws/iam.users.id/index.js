import React from 'react';
import PropTypes from 'prop-types';
import get from 'lodash/get';
import isEmpty from 'lodash/isEmpty';

import { 
  partialDataShape,
  formatDate,
  valueOrNone,
  renderResourcesAsList,
  renderAwsTags,
} from '../../../utils/Partials';
import { Partial, PartialValue } from '../../../components/Partial';
import { TabsMenu, TabPane } from '../../../components/Partial/PartialTabs';
import InformationsWrapper from '../../../components/InformationsWrapper';
import AuthenticationMethods from './AuthenticationMethods';
import Policy from '../../../components/Partial/Policy';


const propTypes = {
  data: PropTypes.shape(partialDataShape).isRequired,
};

const IamUsers = props => {
  const { data } = props;

  if (!data) return null;

  const groups = get(data, ['item', 'groups']);
  const inline_policies = get(data, ['item', 'inline_policies']);
  const policies = get(data, ['item', 'policies']);
  const tags = get(data, ['item', 'Tags']);

  return (
    <Partial data={data}>
      <InformationsWrapper>
        <PartialValue 
          label="ARN" 
          valuePath="arn"
          renderValue={valueOrNone}
        />
        <PartialValue 
          label="Creation Date" 
          valuePath="CreateDate"
          renderValue={formatDate}
        />
      </InformationsWrapper>

      <TabsMenu>
        <TabPane title="Authentication Methods">
          <AuthenticationMethods 
            mfaDevices={get(data, ['item', 'MFADevices'])}
            accessKeys={get(data, ['item', 'AccessKeys'])}
            loginProfile={get(data, ['item', 'LoginProfile'])}
          />
        </TabPane>
        {!isEmpty(groups) && (
          <TabPane title="Groups">
            {renderResourcesAsList(Object.values(groups))}
          </TabPane>
        )}
        {!isEmpty(inline_policies) && (
          <TabPane title="Inline Policies">
            <>
              {Object.entries(inline_policies).map(([id, policy], i) => (
                <Policy
                  key={i}
                  name={policy.name}
                  policy={policy.PolicyDocument}
                  policyPath={`inline_policies.${id}.PolicyDocument`}
                />
              ))}
            </>
          </TabPane>
        )}
        {!isEmpty(policies) && (
          <TabPane title="Managed Policies">
            {renderResourcesAsList(Object.values(policies))}
          </TabPane>
        )}
        {!isEmpty(tags) && (
          <TabPane title="Tags">
            {renderAwsTags(tags)}
          </TabPane>
        )}
      </TabsMenu>
    </Partial>
  );
};

IamUsers.propTypes = propTypes;

export default IamUsers;
