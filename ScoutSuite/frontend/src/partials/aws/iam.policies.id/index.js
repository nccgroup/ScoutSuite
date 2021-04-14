import React from 'react';
import PropTypes from 'prop-types';
import get from 'lodash/get';

import { 
  partialDataShape,
  renderList,
  renderResourceLink,
} from '../../../utils/Partials';
import { Partial } from '../../../components/Partial';
import { TabsMenu, TabPane } from '../../../components/Partial/PartialTabs';
import Policy from '../../../components/Partial/Policy';


const propTypes = {
  data: PropTypes.shape(partialDataShape).isRequired,
};

const IamPolicies = props => {
  const { data } = props;

  if (!data) return null;

  const arn = get(data, ['item', 'arn']);
  const policy = get(data, ['item', 'PolicyDocument'], {});
  const attachedEntities = get(data, ['item', 'attached_to'], {});

  return (
    <Partial data={data}>
      <TabsMenu>
        <TabPane title="Policy">
          <Policy
            name={arn}
            policy={policy}
            policyPath="PolicyDocument"
            defaultOpen
          />
        </TabPane>
        <TabPane title="Attached Entities">
          <ul>
            {Object.entries(attachedEntities).map(([type, entities], i) => (
              <li key={i}>
                {type}
                {renderList(entities, '', renderResourceLink('iam', type))}
              </li>
            ))}
          </ul>
        </TabPane>
      </TabsMenu>
    </Partial>
  );
};

IamPolicies.propTypes = propTypes;

export default IamPolicies;
