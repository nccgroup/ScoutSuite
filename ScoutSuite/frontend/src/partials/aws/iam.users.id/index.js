import React from 'react';
import PropTypes from 'prop-types';
import get from 'lodash/get';
import isEmpty from 'lodash/isEmpty';

import { 
  partialDataShape,
  renderResourcesAsList
} from '../../../utils/Partials';
import { Partial } from '../../../components/Partial';
import { TabsMenu, TabPane } from '../../../components/Tabs';
import Informations from './Informations';
import AuthenticationMethods from './AuthenticationMethods';
import DetailedValue from '../../../components/DetailedValue';
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
      <div className="left-pane">
        <Informations />
      </div>

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
            {renderResourcesAsList(groups)}
          </TabPane>
        )}
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
        {!isEmpty(tags) && (
          <TabPane title="Tags">
            <ul>
              {tags.map((tag, i) => (
                <DetailedValue
                  key={i}
                  label={tag.Key}
                  value={tag.Value}
                />
              ))}
            </ul>
          </TabPane>
        )}
      </TabsMenu>
    </Partial>
  );
};

IamUsers.propTypes = propTypes;

export default IamUsers;
