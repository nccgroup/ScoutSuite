import React from 'react';
import PropTypes from 'prop-types';

import { Partial, PartialValue } from '../../../components/Partial';
import { partialDataShape, formatDate } from '../../../utils/Partials';
import { TabsMenu, TabPane } from '../../../components/Tabs';
import { convertBoolToString } from '../../../utils/Partials/index';
import PartialConditional from '../../../components/Partial/PartialConditional/index';
import PartialList from '../../../components/Partial/PartialList';

const propTypes = {
  data: PropTypes.shape(partialDataShape).isRequired,
};

const renderTraffic = (item, i) => (
  <li key={i}>
    <PartialValue errorPath='' value={item.key} />
    <ul>
      {item.item.map((port, index) => (
        <li key={index}>
          <PartialValue
            errorPath={`${item.key}.${index}.permissive_ports`}
            value={port}
          />
        </li>
      ))}
      {item.item.length === 0 && <li>None</li>}
    </ul>
  </li>
);

const Firewalls = (props) => {
  const { data } = props;

  if (!data) return null;

  return (
    <Partial data={data}>
      <div className="partial-informations">
        <PartialValue label="Firewall name" valuePath="name" />

        <PartialValue label="Project ID" valuePath="project_id" />

        <PartialValue label="Description" valuePath="description" />

        <PartialValue label="Network" valuePath="network" />

        <PartialValue
          label="Creation Date"
          valuePath="creation_timestamp"
          renderValue={formatDate}
        />

        <PartialValue label="Priority" valuePath="priority" />

        <PartialValue
          label="Disabled"
          valuePath="disabled"
          renderValue={convertBoolToString}
        />
      </div>

      <TabsMenu>
        <TabPane title="Configuration">
          <div>
            <PartialValue label="Direction" valuePath="direction" />
            <PartialValue label="Action" valuePath="action" />

            <PartialConditional valuePath="source_ranges">
              <PartialValue errorPath="source_ranges" value="Source Ranges:" />
              <PartialList valuePath="source_ranges" />
            </PartialConditional>

            <PartialConditional valuePath="destination_ranges">
              <PartialValue
                errorPath="destination_ranges"
                value="Destination Ranges:"
              />
              <PartialList valuePath="destination_ranges" />
            </PartialConditional>

            <PartialConditional valuePath="source_tags">
              <PartialValue errorPath="source_tags" value="Source Tags:" />
              <PartialList valuePath="source_tags" />
            </PartialConditional>

            <PartialConditional valuePath="target_tags">
              <PartialValue errorPath="target_tags" value="Target Tags:" />
              <PartialList valuePath="target_tags" />
            </PartialConditional>
          </div>
        </TabPane>

        <TabPane
          title="Allowed Traffic"
          condition={{ valuePath: 'action', eq: 'allowed' }}
        >
          <PartialList
            valuePath="allowed_traffic"
            renderItem={renderTraffic}
          />
        </TabPane>

        <TabPane
          title="Denied Traffic"
          condition={{ valuePath: 'action', neq: 'allowed' }}
        >
          <PartialList
            valuePath="denied_traffic"
            renderItem={renderTraffic}
          />
        </TabPane>
      </TabsMenu>
    </Partial>
  );
};

Firewalls.propTypes = propTypes;

export default Firewalls;
