import React from 'react';
import PropTypes from 'prop-types';

import { Partial, PartialSection, PartialValue } from '../../../components/Partial';
import { partialDataShape, formatDate } from '../../../utils/Partials';
import { TabsMenu, TabPane } from '../../../components/Tabs';
import { convertBoolToString } from '../../../utils/Partials/index';
import get from 'lodash/get';

const propTypes = {
  data: PropTypes.shape(partialDataShape).isRequired,
};

const renderTraffic = (items) => {
  const traffic = Object.entries(items);

  return <ul>
    {traffic.map(([key, value]) => <li key={key}>
      <PartialValue errorPath={key} value={key} />
      <ul>
        {value.map((port, index) => (
          <li key={index}>
            <PartialValue
              errorPath={`${key}.${index}.permissive_ports`}
              value={port}
            />
          </li>
        ))}
        {value.length === 0 && <li>None</li>}
      </ul>
    </li>)}
  </ul>;
};

const renderList = (items) => (
  <ul>
    {items.map((item, key) => (
      <li key={key}>{item}</li>
    ))}
  </ul>
);

const Firewalls = (props) => {
  const { data } = props;

  if (!data) return null;

  const item = get(data, ['item'], {});

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

            {item.source_ranges && (
              <>
                <PartialValue
                  errorPath="source_ranges"
                  value="Source Ranges:"
                />
                {renderList(item.source_ranges)}
              </>
            )}

            {item.destination_ranges && (
              <>
                <PartialValue
                  errorPath="destination_ranges"
                  value="Destination Ranges:"
                />
                {renderList(item.source_ranges)}
              </>
            )}

            {item.source_tags && (
              <>
                <PartialValue errorPath="source_tags" value="Source Tags:" />
                {renderList(item.source_tags)}
              </>
            )}

            {item.target_tags && (
              <>
                <PartialValue errorPath="target_tags" value="Target Tags:" />
                {renderList(item.target_tags)}
              </>
            )}
          </div>
        </TabPane>

        {item.action === 'allowed' && (
          <TabPane title="Allowed Traffic">
            <PartialSection path="allowed_traffic">
              {renderTraffic(item.allowed_traffic)}
            </PartialSection>
          </TabPane>
        )}

        {item.action !== 'allowed' && (
          <TabPane title="Denied Traffic">
            <PartialSection path="denied_traffic">
              {renderTraffic(item.denied_traffic)}
            </PartialSection>
          </TabPane>
        )}
      </TabsMenu>
    </Partial>
  );
};

Firewalls.propTypes = propTypes;

export default Firewalls;
