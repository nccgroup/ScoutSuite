import React from 'react';
import PropTypes from 'prop-types';

import InformationsWrapper from '../../../components/InformationsWrapper';
import { Partial, PartialValue } from '../../../components/Partial';
import { partialDataShape, valueOrNone } from '../../../utils/Partials';
import { TabsMenu, TabPane } from '../../../components/Partial/PartialTabs';
import { renderList } from '../../../utils/Partials/index';
import ResourceLink from '../../../components/ResourceLink/index';
import { useResources } from '../../../api/useResources';
import Policy from '../../../components/Partial/Policy';

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

const renderServicePrincipals = service_principals => {
  const renderSP = sp => (
    <ResourceLink
      service="aad"
      resource="service_principals"
      id={sp.id}
      name={sp.name}
    />
  );
  return renderList(service_principals, '', sp => renderSP(sp));
};

const propTypes = {
  data: PropTypes.shape(partialDataShape).isRequired,
  item: PropTypes.object,
};

const Roles = props => {
  const { data, item } = props;
  const { data: users } = useResources(
    'aad',
    'users',
    item.assignments ? item.assignments.users : [],
  );
  const { data: groups } = useResources(
    'aad',
    'groups',
    item.assignments ? item.assignments.groups : [],
  );
  const { data: service_principals } = useResources(
    'aad',
    'service_principals',
    item.assignments ? item.assignments.service_principals : [],
  );

  if (!data) return null;

  return (
    <Partial data={data}>
      <InformationsWrapper>
        <PartialValue
          label="ID" valuePath="id"
          renderValue={valueOrNone} />

        <PartialValue
          label="Description"
          valuePath="description"
          renderValue={valueOrNone}
        />

        <PartialValue
          label="Type" valuePath="type"
          renderValue={valueOrNone} />

        <PartialValue
          label="Role Type"
          valuePath="role_type"
          renderValue={valueOrNone}
        />

        <PartialValue
          label="Assignable Scopes"
          valuePath="assignable_scopes"
          renderValue={valueOrNone}
        />
        <PartialValue
          label="Custom Subscriptions Owner Roles"
          valuePath="custom_subscription_owner_role"
        />
      </InformationsWrapper>

      <TabsMenu>
        <TabPane title="Permissions">
          <Policy
            name=''
            policy={item.permissions}
            defaultOpen
          />
        </TabPane>
        <TabPane title="Assignments">
          {item.assignments.users && <>
            <PartialValue
              label="Users"
              errorPath="users"
              value="" />
            <ul>
              {renderUsers(users)}
            </ul>
          </>}

          {item.assignments.groups && <>
            <PartialValue
              label="Groups"
              errorPath="groups"
              value="" />
            <ul>
              {renderGroups(groups)}
            </ul>
          </>}

          {item.assignments.service_principals && <>
            <PartialValue
              label="Service Principals"
              errorPath="serviceprincipals"
              value="" />
            <ul>
              {renderServicePrincipals(service_principals)}
            </ul>
          </>}
        </TabPane>
      </TabsMenu>
    </Partial>
  );
};

Roles.propTypes = propTypes;

export default Roles;
