import React from 'react';
import PropTypes from 'prop-types';

import { Partial, PartialValue } from '../../../components/Partial';
import { partialDataShape } from '../../../utils/Partials';
import { TabsMenu, TabPane } from '../../../components/Tabs';
import { renderList } from '../../../utils/Partials/index';
import InformationsWrapper from '../../../components/InformationsWrapper';

const propTypes = {
  data: PropTypes.shape(partialDataShape).isRequired,
};

const Users = props => {
  const { data } = props;

  if (!data) return null;

  return (
    <Partial data={data}>
      <InformationsWrapper>
        <PartialValue
          label="User"
          valuePath="name" />

        <PartialValue
          label="Project ID"
          errorPath="project_id"
          valuePath="project_id"
        />
      </InformationsWrapper>

      <TabsMenu>
        <TabPane title="Bindings">
          <PartialValue
            valuePath="roles"
            renderValue={renderList} />
        </TabPane>
      </TabsMenu>
    </Partial>
  );
};

Users.propTypes = propTypes;

export default Users;
