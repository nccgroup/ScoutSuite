import React from 'react';
import PropTypes from 'prop-types';
import get from 'lodash/get';
import isEmpty from 'lodash/isEmpty';

import { 
  partialDataShape, 
  renderResourcesAsList 
} from '../../../utils/Partials';
import { Partial } from '../../../components/Partial';
import { TabsMenu, TabPane } from '../../../components/Partial/PartialTabs';
import Informations from '../iam.users.id/Informations';
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
        <Informations />
      </div>

      <TabsMenu>
        <TabPane title="Members">
          {!isEmpty(members) ? (
            renderResourcesAsList(members)
          ) : (
            <WarningMessage message="This group has no members."/>
          )}
        </TabPane>
        {!isEmpty(inline_policies) && (
          <TabPane title="Inline Policies">
            <>
              {Object.values(inline_policies).map((policy, i) => (
                <Policy
                  key={i}
                  name={policy.name}
                  policy={policy.PolicyDocument}
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
