import React from 'react';
import PropTypes from 'prop-types';

import { Partial, PartialValue } from '../../../components/Partial';
import { partialDataShape, formatDate } from '../../../utils/Partials';
import { TabsMenu, TabPane } from '../../../components/Tabs';
import { convertBoolToString } from '../../../utils/Partials/index';
import get from 'lodash/get';

const propTypes = {
  data: PropTypes.shape(partialDataShape).isRequired,
};

const renderTraffic = (item, i) => (
  <li key={i}>
    <PartialValue errorPath="" value={item.key} />
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
            {renderTraffic(item.allowed_traffic)}
          </TabPane>
        )}

        {item.action !== 'allowed' && (
          <TabPane title="Denied Traffic">
            {renderTraffic(item.denied_traffic)}
          </TabPane>
        )}
      </TabsMenu>
    </Partial>
  );
};

Firewalls.propTypes = propTypes;

export default Firewalls;
