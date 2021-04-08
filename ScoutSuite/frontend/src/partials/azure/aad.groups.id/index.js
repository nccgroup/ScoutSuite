import React, { useMemo } from 'react';
import PropTypes from 'prop-types';

import InformationsWrapper from '../../../components/InformationsWrapper';
import { Partial, PartialValue } from '../../../components/Partial';
import {
  partialDataShape,
  valueOrNone,
  convertBoolToEnable,
} from '../../../utils/Partials';
import { TabsMenu, TabPane } from '../../../components/Partial/PartialTabs';
import { useResources } from '../../../api/useResources';
import { renderList } from '../../../utils/Partials/index';
import ResourceLink from '../../../components/ResourceLink/index';

const renderUsers = users => {
  const renderUser = user => (
    <ResourceLink
      service="aad"
      resource="users"
      id={user.id}
      name={user.name}
    />
  );
  return renderList(users, '', user => renderUser(user));
};

const renderRoles = (roles, rolesList) => {
  const renderRole = role => {
    const { subscription_id } = rolesList.find(r => r.role_id === role.id);
    return (
      <span>
        <ResourceLink
          service="rbac"
          resource="roles"
          id={role.id}
          name={role.name}
        />{' '}
        (subscription {subscription_id})
      </span>
    );
  };
  return renderList(roles, '', role => renderRole(role));
};

const propTypes = {
  data: PropTypes.shape(partialDataShape).isRequired,
  item: PropTypes.object,
};

const Groups = props => {
  const { data, item } = props;
  const { data: users } = useResources('aad', 'users', item.users);
  const rolesList = useMemo(() => item.roles.map(r => r.role_id), [item.roles]);
  const { data: roles } = useResources('rbac', 'roles', rolesList);

  if (!data) return null;

  return (
    <Partial data={data}>
      <InformationsWrapper>
        <PartialValue
          label="Name" valuePath="name"
          renderValue={valueOrNone} />

        <PartialValue
          label="Type"
          valuePath="object_type"
          renderValue={valueOrNone}
        />

        <PartialValue
          label="Mail Nickname"
          valuePath="mail_nickname"
          renderValue={valueOrNone}
        />

        <PartialValue
          label="Mail Status"
          valuePath="mail_enabled"
          renderValue={convertBoolToEnable}
        />

        <PartialValue
          label="Mail" valuePath="mail"
          renderValue={valueOrNone} />

        <PartialValue
          label="Security Status"
          valuePath="security_enabled"
          renderValue={convertBoolToEnable}
        />

        <PartialValue
          label="Deletion Timestamp"
          valuePath="deletion_timestamp"
          renderValue={valueOrNone}
        />
      </InformationsWrapper>

      <TabsMenu>
        <TabPane title="Role Assignments">
          {renderRoles(roles, item.roles)}
        </TabPane>

        <TabPane title="Members">{renderUsers(users)}</TabPane>
      </TabsMenu>
    </Partial>
  );
};

Groups.propTypes = propTypes;

export default Groups;
