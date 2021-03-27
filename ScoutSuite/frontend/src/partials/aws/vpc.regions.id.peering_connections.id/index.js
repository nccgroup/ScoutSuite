
import React from 'react';
import PropTypes from 'prop-types';
import get from 'lodash/get';
import isEmpty from 'lodash/isEmpty';

import { partialDataShape } from '../../../utils/Partials';
import { Partial, PartialValue } from '../../../components/Partial';
import { TabsMenu, TabPane } from '../../../components/Partial/PartialTabs';
import PeeringConnection from './PeeringConnection';
import DetailedValue from '../../../components/DetailedValue';


const propTypes = {
  data: PropTypes.shape(partialDataShape).isRequired,
};

const RegionDomain = props => {
  const { data } = props;

  if (!data) return null;

  const requesterInfos = get(data, ['item', 'RequesterVpcInfo']);
  const accepterInfos = get(data, ['item', 'AccepterVpcInfo']);
  const tags = get(data, ['item', 'Tags'], []);

  return (
    <Partial data={data}>
      <div className="left-pane">
        <h4>Informations</h4>
        <PartialValue 
          label="Status"
          valuePath="Status.Message"
        />
      </div>

      <TabsMenu>
        <TabPane title="Requester VPC">
          <PeeringConnection connectionInfos={requesterInfos} />
        </TabPane>
        <TabPane title="Accepter VPC">
          <PeeringConnection connectionInfos={accepterInfos} />
        </TabPane>
        <TabPane 
          title="Tags"
          disabled={isEmpty(tags)}
        >
          <ul>
            {tags.map((tag, i) => (
              <li key={i}>
                <DetailedValue
                  label={tag.Key}
                  value={tag.Value}
                />
              </li>
            ))}
          </ul>
        </TabPane>
      </TabsMenu>
    </Partial>
  );
};

RegionDomain.propTypes = propTypes;

export default RegionDomain;
