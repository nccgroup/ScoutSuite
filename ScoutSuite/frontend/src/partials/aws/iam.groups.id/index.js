import React from 'react';
import PropTypes from 'prop-types';
import get from 'lodash/get';
import isEmpty from 'lodash/isEmpty';

import { 
  partialDataShape,
  formatDate,
  valueOrNone,
  renderList,
  renderPolicyLink,
} from '../../../utils/Partials';
import { Partial, PartialValue } from '../../../components/Partial';
import { TabsMenu, TabPane } from '../../../components/Partial/PartialTabs';
import InformationsWrapper from '../../../components/InformationsWrapper';
import WarningMessage from '../../../components/WarningMessage';
import Policy from '../../../components/Partial/Policy';
import ResourceLink from '../../../components/ResourceLink';


const propTypes = {
  data: PropTypes.shape(partialDataShape).isRequired,
};

const IamGroups = props => {
  const { data } = props;

  if (!data) return null;

  const users = get(data, ['item', 'users'], []);
  const inline_policies = get(data, ['item', 'inline_policies'], {});
  const policies = get(data, ['item', 'policies'], []);

  const renderUserLink = id => (
    <ResourceLink
      service="iam"
      resource="users"
      id={id}
    />
  );

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
        <TabPane title="Members">
          {!isEmpty(users) ? (
            renderList(users, '', renderUserLink)
          ) : (
            <PartialValue
              errorPath="ALL"
              renderValue={() => (
                <WarningMessage message="This group has no members."/>
              )}
            />
          )}
        </TabPane>
        <TabPane 
          title="Inline Policies"
          disabled={isEmpty(inline_policies)}
        >
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
        <TabPane 
          title="Managed Policies"
          disabled={isEmpty(policies)}
        >
          {renderList(policies, '', renderPolicyLink)}
        </TabPane>
      </TabsMenu>
    </Partial>
  );
};

IamGroups.propTypes = propTypes;

export default IamGroups;
