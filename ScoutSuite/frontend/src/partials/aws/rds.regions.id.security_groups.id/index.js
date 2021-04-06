
import React from 'react';
import PropTypes from 'prop-types';
import get from 'lodash/get';
import isEmpty from 'lodash/isEmpty';

import { partialDataShape } from '../../../utils/Partials';
import { Partial, PartialValue } from '../../../components/Partial';
import { TabsMenu, TabPane } from '../../../components/Partial/PartialTabs';
import InformationsWrapper from '../../../components/InformationsWrapper';


const propTypes = {
  data: PropTypes.shape(partialDataShape).isRequired,
};

const SecurityGroups = props => {
  const { data } = props;

  if (!data) return null;

  const groups = get(data, ['item', 'EC2SecurityGroups']);
  const ipRanges = get(data, ['item', 'IPRanges']);

  return (
    <Partial data={data}>
      <InformationsWrapper>
        <PartialValue
          label="Descripition"
          valuePath="DBSecurityGroupDescription"
        />
      </InformationsWrapper>

      <TabsMenu>
        <TabPane 
          title="Authorizations"
          disabled={isEmpty(groups)}
        >
          <ul>
            {groups.map((
              {
                EC2SecurityGroupName: name,
                EC2SecurityGroupId: groupId,
                EC2SecurityGroupOwnerId: ownerId,
                Status,
              }, i
            ) => (
              <li key={i}>
                {`${name} (${groupId}) @ ${ownerId} (${Status})`}
              </li>
            ))}
            {ipRanges.map((range, i) => (
              <li key={i}>
                {`${range.CIDRIP} (${range.Status})`}
              </li>
            ))}
          </ul>
        </TabPane>
      </TabsMenu> 
    </Partial>
  );
};

SecurityGroups.propTypes = propTypes;

export default SecurityGroups;
