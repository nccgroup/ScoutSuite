import React from 'react';
import PropTypes from 'prop-types';
import get from 'lodash/get';
import isEmpty from 'lodash/isEmpty';

import { 
  partialDataShape,
  renderList,
  renderResourceLink,
  renderPolicyLink,
  renderAwsTags,
} from '../../../utils/Partials';
import { Partial } from '../../../components/Partial';
import { TabsMenu, TabPane } from '../../../components/Partial/PartialTabs';
import InformationsWrapper from '../../../components/InformationsWrapper';
import Informations from './Informations';
import Policy from '../../../components/Partial/Policy';


const propTypes = {
  data: PropTypes.shape(partialDataShape).isRequired,
};

const IamRoles = props => {
  const { data } = props;

  if (!data) return null;

  const role_policy = get(data, ['item', 'assume_role_policy'], {});
  const instances = get(data, ['item', 'instance_profiles'], {});
  const lambdas = get(data, ['item', 'awslambdas'], {});
  const inline_policies = get(data, ['item', 'inline_policies'], {});
  const policies = get(data, ['item', 'policies'], []);
  const tags = get(data, ['item', 'Tags'], []);

  return (
    <Partial data={data}>
      <InformationsWrapper>
        <Informations />
      </InformationsWrapper>

      <TabsMenu>
        <TabPane title="Role Trust Policy">
          <Policy
            policy={role_policy.PolicyDocument}
            policyPath="assume_role_policy.PolicyDocument"
          />
        </TabPane>
        <TabPane 
          title="Instances"
          disabled={isEmpty(instances)}
        >
          {renderList(Object.values(instances), '', renderResourceLink('ec2', 'instances'))}
        </TabPane>
        <TabPane 
          title="Lambda Functions"
          disabled={isEmpty(lambdas)}
        >
          {renderList(Object.values(lambdas), '', renderResourceLink('awslambda', 'functions'))}
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
        <TabPane 
          title="Tags"
          disabled={isEmpty(tags)}
        >
          {renderAwsTags(tags)}
        </TabPane>
      </TabsMenu>
    </Partial>
  );
};

IamRoles.propTypes = propTypes;

export default IamRoles;
