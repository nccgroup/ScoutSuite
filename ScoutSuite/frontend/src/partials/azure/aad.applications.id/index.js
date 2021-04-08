import React from 'react';
import PropTypes from 'prop-types';

import InformationsWrapper from '../../../components/InformationsWrapper';
import { Partial, PartialValue } from '../../../components/Partial';
import { partialDataShape, valueOrNone } from '../../../utils/Partials';
import { TabsMenu, TabPane } from '../../../components/Partial/PartialTabs';
import { renderList } from '../../../utils/Partials/index';

const renderPasswordCredentials = (item) => {
  return (
    <li key={item.id}>
      <PartialValue label="ID" value={item.key_id} />
      <ul>
        <li><PartialValue label="Start Date" value={item.start_date} /></li>
        <li><PartialValue label="End Date" value={item.end_date} /></li>
      </ul>
    </li>
  );
};

const propTypes = {
  data: PropTypes.shape(partialDataShape).isRequired,
};

const Applications = props => {
  const { data } = props;

  if (!data) return null;

  return (
    <Partial data={data}>
      <InformationsWrapper>
        <PartialValue
          label="ID" valuePath="id"
          renderValue={valueOrNone} />

        <PartialValue
          label="App ID"
          valuePath="app_id"
          renderValue={valueOrNone}
        />

        <PartialValue
          label="Type"
          valuePath="object_type"
          renderValue={valueOrNone}
        />

        <PartialValue
          label="Sign In Audience"
          valuePath="sign_in_audience"
          renderValue={valueOrNone}
        />

        <PartialValue
          label="Publisher Domain"
          valuePath="publisher_domain"
          renderValue={valueOrNone}
        />

        <PartialValue
          label="Available To Other Tenants"
          valuePath="available_to_other_tenants"
          renderValue={valueOrNone}
        />

        <PartialValue
          label="Allow Guests Sign-In"
          valuePath="allow_guests_sign_in"
          renderValue={valueOrNone}
        />

        <PartialValue
          label="Allow Passthrough Users"
          valuePath="allow_passthrough_users"
          renderValue={valueOrNone}
        />

        <PartialValue
          label="Public Client"
          valuePath="public_client"
          renderValue={valueOrNone}
        />

        <PartialValue
          label="Device-Only Auth Supported"
          valuePath="is_device_only_auth_supported"
          renderValue={valueOrNone}
        />

        <PartialValue
          label="Pre-Authorized Applications"
          valuePath="pre_authorized_applications"
          renderValue={valueOrNone}
        />

        <PartialValue
          label="Deletion Timestamp"
          valuePath="deletion_timestamp"
          renderValue={valueOrNone}
        />
      </InformationsWrapper>

      <TabsMenu>
        <TabPane title="Password Credentials">
          <PartialValue
            valuePath="password_credentials"
            renderValue={values =>
              renderList(values, '', renderPasswordCredentials)
            }
          />
        </TabPane>
      </TabsMenu>
    </Partial>
  );
};

Applications.propTypes = propTypes;

export default Applications;
