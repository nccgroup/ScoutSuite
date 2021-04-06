import React from 'react';
import PropTypes from 'prop-types';
import get from 'lodash/get';
import isEmpty from 'lodash/isEmpty';

import { 
  partialDataShape, 
  renderResourcesAsList, 
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

const IamGroups = props => {
  const { data } = props;

  if (!data) return null;

  const role_policy = get(data, ['item', 'assume_role_policy']);
  const instances = get(data, ['item', 'instance_profiles']);
  const lambdas = get(data, ['item', 'awslambdas']);
  const inline_policies = get(data, ['item', 'inline_policies']);
  const policies = get(data, ['item', 'policies']);
  const tags = get(data, ['item', 'Tags']);

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
        {!isEmpty(instances) && (
          <TabPane title="Instances">
            {renderResourcesAsList(Object.values(instances), 'name')}
          </TabPane>
        )}
        {!isEmpty(lambdas) && (
          <TabPane title="Lambda Functions">
            {renderResourcesAsList(Object.values(lambdas), 'name')}
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

IamGroups.propTypes = propTypes;

export default IamGroups;
