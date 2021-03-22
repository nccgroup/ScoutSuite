import React from 'react';
import PropTypes from 'prop-types';

import { Partial, PartialValue } from '../../../components/Partial';
import { partialDataShape, valueOrNone, renderList } from '../../../utils/Partials';
import { TabsMenu, TabPane } from '../../../components/Tabs';

const propTypes = {
  data: PropTypes.shape(partialDataShape).isRequired,
};

const Bindings = props => {
  const { data } = props;

  if (!data) return null;

  return (
    <Partial data={data}>
      <div className="left-pane">
        <PartialValue
          label="Title"
          valuePath="title" />

        <PartialValue
          label="Description"
          valuePath="description"
          renderValue={valueOrNone}
        />

        <PartialValue
          label="Project ID"
          errorPath="projet_id"
          valuePath="project"
        />

        <PartialValue
          label="Custom Role"
          valuePath="custom_role"
          renderValue={valueOrNone} />
      </div>

      <TabsMenu>
        <TabPane title="Permissions"></TabPane>

        <TabPane title="Bindings">
          <PartialValue
            label="Attached Users"
            valuePath="members.users"
            renderValue={renderList}
          />

          <PartialValue
            label="Attached Groups"
            valuePath="members.groups"
            renderValue={renderList}
          />

          <PartialValue
            label="Attached Service Accounts"
            valuePath="members.service_accounts"
            renderValue={renderList}
          />
        </TabPane>
      </TabsMenu>
    </Partial>
  );
};

Bindings.propTypes = propTypes;

export default Bindings;
