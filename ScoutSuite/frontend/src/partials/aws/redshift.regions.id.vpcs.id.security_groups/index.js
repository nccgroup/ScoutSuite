
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

  const ipRanges = get(data, ['item', 'IPRanges']);
  const groups = get(data, ['item', 'EC2SecurityGroups']);

  return (
    <Partial data={data}>
      <InformationsWrapper>
        <PartialValue
          label="Descripition"
          valuePath="Description"
        />
      </InformationsWrapper>

      <TabsMenu>
        <TabPane 
          title="Rules"
          disabled={isEmpty(ipRanges) && isEmpty(groups)}
        >
          {!isEmpty(ipRanges) && (
            <ul>
              IP Addresses:
              {ipRanges.map((range, i) => (
                <li key={i}>
                  <PartialValue
                    label={range.CIDRIP}
                    value={range.Status}
                  />
                </li>
              ))}
            </ul>
          )}
          {!isEmpty(groups) && (
            <ul>
              EC2 Security Groups:
              {groups.map((
                {
                  CIDRIP,
                  EC2SecurityGroupName: name,
                  UserId,
                  Status,
                }, i
              ) => (
                <li key={i}>
                  <PartialValue
                    label={CIDRIP}
                    value={`${name} (AWS account ID: ${UserId}): ${Status}`}
                  />
                </li>
              ))}
            </ul>
          )}
        </TabPane>
      </TabsMenu> 
    </Partial>
  );
};

SecurityGroups.propTypes = propTypes;

export default SecurityGroups;
