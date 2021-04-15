import React from 'react';
import PropTypes from 'prop-types';

import InformationsWrapper from '../../../components/InformationsWrapper';
import { Partial, PartialValue } from '../../../components/Partial';
import {
  partialDataShape,
  valueOrNone,
  convertBoolToEnable,
} from '../../../utils/Partials';
import { TabsMenu, TabPane } from '../../../components/Partial/PartialTabs';
import { renderList } from '../../../utils/Partials/index';
import ResourceLink from '../../../components/ResourceLink/index';
import { useResources } from '../../../api/useResources';

const renderGroups = groups => {
  const renderGroup = group => (
    <ResourceLink
      service="aad"
      resource="groups"
      id={group.id}
      name={group.name}
    />
  );
  return renderList(groups, '', group => renderGroup(group));
};

const propTypes = {
  data: PropTypes.shape(partialDataShape).isRequired,
  item: PropTypes.object,
};

const Users = props => {
  const { data, item } = props;
  const { data: groups } = useResources('aad', 'groups', item.groups);

  if (!data) return null;

  return (
    <Partial data={data}>
      <InformationsWrapper>
        <PartialValue
          label="Principal Name"
          valuePath="name"
          renderValue={valueOrNone}
        />

        <PartialValue
          label="Display Name"
          valuePath="display_name"
          renderValue={valueOrNone}
        />

        <PartialValue
          label="Given Name"
          valuePath="given_name"
          renderValue={valueOrNone}
        />

        <PartialValue
          label="Surname"
          valuePath="surname"
          renderValue={valueOrNone}
        />

        <PartialValue
          label="Mail Nickname"
          valuePath="mail_nickname"
          renderValue={valueOrNone}
        />

        <PartialValue
          label="Mail" valuePath="mail"
          renderValue={valueOrNone} />

        <PartialValue
          label="Sign-In Names"
          valuePath="sign_in_names"
          renderValue={valueOrNone}
        />

        <PartialValue
          label="Type"
          valuePath="user_type"
          renderValue={valueOrNone}
        />

        <PartialValue
          label="Status"
          valuePath="account_enabled"
          renderValue={convertBoolToEnable}
        />

        <PartialValue
          label="Usage Location"
          valuePath="usage_location"
          renderValue={valueOrNone}
        />

        <PartialValue
          label="Deletion Timestamp"
          valuePath="deletion_timestamp"
          renderValue={valueOrNone}
        />
      </InformationsWrapper>

      <TabsMenu>
        <TabPane
          title="Groups"
        >
          {renderGroups(groups)}
        </TabPane>
      </TabsMenu>
    </Partial>
  );
};

Users.propTypes = propTypes;

export default Users;
