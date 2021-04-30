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

const Groups = props => {
  const { data } = props;

  if (!data) return null;

  return (
    <Partial data={data}>
      <InformationsWrapper>
        <PartialValue
          label="Group"
          valuePath="name" />

        <PartialValue
          label="Project ID"
          errorPath="project_id"
          valuePath="project" />
      </InformationsWrapper>

      <TabsMenu>
        <TabPane title="Bindings">
          <PartialValue
            label="Roles"
            valuePath="roles"
            renderValue={renderList} />
        </TabPane>
      </TabsMenu>
    </Partial>
  );
};

Groups.propTypes = propTypes;

export default Groups;
