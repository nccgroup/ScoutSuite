import React from 'react';
import PropTypes from 'prop-types';
import get from 'lodash/get';

import { Partial, PartialValue } from '../../../components/Partial';
import { partialDataShape } from '../../../utils/Partials';
import { TabsMenu, TabPane } from '../../../components/Tabs';
import PartialSection from '../../../components/Partial/PartialSection/index';
import { formatDate, renderList } from '../../../utils/Partials/index';

const renderKeys = keys => {
  if (!keys || keys.length === 0) return <span>None</span>;

  return (
    <ul>
      {Object.entries(keys).map(([key]) => (
        <PartialSection
          path={`keys.${key}`}
          key={key}>
          <li>
            <b>{key}</b>
            <ul>
              <li>
                <PartialValue
                  label="Key Type"
                  valuePath="key_type" />
              </li>
              <li>
                <PartialValue
                  label="Key Algorithm"
                  valuePath="key_algorithm" />
              </li>
              <li>
                <PartialValue
                  label="Valid Before"
                  valuePath="valid_before"
                  renderValue={formatDate}
                />
              </li>
              <li>
                <PartialValue
                  label="Valid After"
                  valuePath="valid_after"
                  renderValue={formatDate}
                />
              </li>
            </ul>
          </li>
        </PartialSection>
      ))}
    </ul>
  );
};

const renderBindings = bindings => {
  if (!bindings || bindings.length === 0) return <span>None</span>;

  return (
    <ul>
      {Object.values(bindings).map((binding, i) => (
        <li key={i}>
          <b>{binding.role}</b>
          <ul>{renderList(binding.members)}</ul>
        </li>
      ))}
    </ul>
  );
};

const propTypes = {
  data: PropTypes.shape(partialDataShape).isRequired,
};

const ServiceAccounts = props => {
  const { data } = props;
  const item = get(data, ['item'], {});

  if (!data) return null;

  return (
    <Partial data={data}>
      <div className="left-pane">
        <PartialValue
          label="ID"
          valuePath="id" />

        <PartialValue
          label="Project ID"
          valuePath="project_id" />

        <PartialValue
          label="Email"
          valuePath="email" />

        <PartialValue
          label="Display Name"
          valuePath="display_name" />

        <PartialValue
          label="Default Service Account"
          valuePath="default_service_account"
        />
      </div>

      <TabsMenu>
        <TabPane title="Keys">{renderKeys(item.keys)}</TabPane>

        <TabPane title="Service Account Users">
          {renderBindings(item.bindings)}
        </TabPane>
      </TabsMenu>
    </Partial>
  );
};

ServiceAccounts.propTypes = propTypes;

export default ServiceAccounts;
