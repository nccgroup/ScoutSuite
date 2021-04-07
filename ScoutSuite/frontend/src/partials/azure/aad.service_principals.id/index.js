import React, { useMemo } from 'react';
import PropTypes from 'prop-types';

import InformationsWrapper from '../../../components/InformationsWrapper';
import { Partial, PartialValue } from '../../../components/Partial';
import {
  partialDataShape,
  valueOrNone,
  renderList,
  convertBoolToEnable,
  formatDate,
} from '../../../utils/Partials';
import { TabsMenu, TabPane } from '../../../components/Partial/PartialTabs';
import ResourceLink from '../../../components/ResourceLink/index';
import { useResources } from '../../../api/useResources';
import PartialSection from '../../../components/Partial/PartialSection';

const renderAppName = (app_name, app_id) => {
  if (!app_name) return <span>None</span>;

  return (
    <ResourceLink
      service="aad"
      resource="applications"
      id={app_id}
      name={app_name}
    />
  );
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

const renderKeys = keys => {
  if (!keys || keys.length === 0) return <span>None</span>;

  return (
    <ul>
      {keys.map((key, index) => (
        <PartialSection
          path={`keys.${index}`}
          key={index}>
          <li>
            <b>{key.key_id}</b>
            <ul>
              <li>
                <PartialValue
                  label="Type"
                  valuePath="type"
                  renderValue={valueOrNone} />
              </li>
              <li>
                <PartialValue
                  label="Usage"
                  valuePath="usage"
                  renderValue={valueOrNone} />
              </li>
              <li>
                <PartialValue
                  label="Start Date"
                  valuePath="start_date"
                  renderValue={formatDate}
                />
              </li>
              <li>
                <PartialValue
                  label="End Date"
                  valuePath="end_date"
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

const propTypes = {
  data: PropTypes.shape(partialDataShape).isRequired,
  item: PropTypes.object,
};

const ServicePrincipals = props => {
  const { data, item } = props;
  const rolesList = useMemo(() => item.roles.map(r => r.role_id), [item.roles]);
  const { data: roles } = useResources('rbac', 'roles', rolesList);

  if (!data) return null;

  return (
    <Partial data={data}>
      <InformationsWrapper>
        <PartialValue
          label="ID" valuePath="id"
          renderValue={valueOrNone} />

        <PartialValue
          label="Tags"
          valuePath="tags"
          renderValue={tags => renderList(tags, valueOrNone)}
        />

        <PartialValue
          label="App"
          valuePath="app_name"
          renderValue={app_name => renderAppName(app_name, item.app_id)}
        />

        <PartialValue
          label="Status"
          valuePath="account_enabled"
          renderValue={convertBoolToEnable}
        />

        <PartialValue
          label="App Owner Tenant ID"
          valuePath="app_owner_tenant_id"
          renderValue={valueOrNone}
        />

        <PartialValue
          label="App Role Assignment Required"
          valuePath="app_role_assignment_required"
          renderValue={valueOrNone}
        />

        <PartialValue
          label="Type"
          valuePath="object_type"
          renderValue={valueOrNone}
        />

        <PartialValue
          label="Service Principal Type"
          valuePath="service_principal_type"
          renderValue={valueOrNone}
        />

        <PartialValue
          label="Publisher Name"
          valuePath="publisher_name"
          renderValue={valueOrNone}
        />

        <PartialValue
          label="Deletion Timestamp"
          valuePath="deletion_timestamp"
          renderValue={valueOrNone}
        />
      </InformationsWrapper>

      <TabsMenu>
        <TabPane title="Roles">
          {renderRoles(roles, item.roles)}
        </TabPane>

        <TabPane title="Keys">
          {renderKeys(item.key_credentials)}
        </TabPane>
      </TabsMenu>
    </Partial>
  );
};

ServicePrincipals.propTypes = propTypes;

export default ServicePrincipals;
