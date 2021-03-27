import React from 'react';
import PropTypes from 'prop-types';
import get from 'lodash/get';
import isEmpty from 'lodash/isEmpty';

import { 
  partialDataShape,
  formatDate,
  valueOrNone,
  renderResourcesAsList,
} from '../../../utils/Partials';
import { Partial, PartialValue } from '../../../components/Partial';
import { TabsMenu, TabPane } from '../../../components/Partial/PartialTabs';
import WarningMessage from '../../../components/WarningMessage';
import Policy from '../../../components/Partial/Policy';


const propTypes = {
  data: PropTypes.shape(partialDataShape).isRequired,
};

const IamGroups = props => {
  const { data } = props;

  if (!data) return null;

  const members = get(data, ['item', 'users'], []);
  const inline_policies = get(data, ['item', 'inline_policies']);
  const policies = get(data, ['item', 'policies']);

  return (
    <Partial data={data}>
      <div className="left-pane">
        <h4>Informations</h4>
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
      </div>

      <TabsMenu>
        <TabPane title="Members">
          {!isEmpty(members) ? (
            renderResourcesAsList(members)
          ) : (
            <PartialValue
              errorPath="ALL"
              renderValue={() => (
                <WarningMessage message="This group has no members."/>
              )}
            />
          )}
        </TabPane>
        {!isEmpty(inline_policies) && (
          <TabPane title="Inline Policies">
            <>
              {Object.entries(inline_policies).map(([id, policy], i) => (
                <Policy
                  key={i}
                  name={policy.name}
                  policy={policy.PolicyDocument}
                  policyPath={`inline_policies.${id}`}
                />
              ))}
            </>
          </TabPane>
        )}
        {!isEmpty(policies) && (
          <TabPane title="Managed Policies">
            {renderResourcesAsList(policies)}
          </TabPane>
        )}
      </TabsMenu>
    </Partial>
  );
};

IamGroups.propTypes = propTypes;

export default IamGroups;
