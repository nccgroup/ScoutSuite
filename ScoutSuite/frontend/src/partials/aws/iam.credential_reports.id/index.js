import React from 'react';
import PropTypes from 'prop-types';

import { partialDataShape, formatDate } from '../../../utils/Partials';
import { Partial, PartialValue } from '../../../components/Partial';


const propTypes = {
  data: PropTypes.shape(partialDataShape).isRequired,
};

const IamCredentialReport = props => {
  const { data } = props;

  if (!data) return null;

  return (
    <Partial data={data}>
      <div>
        <h4>Credentials</h4>
        <PartialValue
          label="Creation Date"
          valuePath="user_creation_time"
          renderValue={formatDate}
        />
        <PartialValue
          label="Last Used Date"
          valuePath="last_used"
          errorPath="inactive_user"
          renderValue={formatDate}
        />
        <PartialValue
          label="Password Enabled"
          valuePath="password_enabled"
          errorPath="unused_credentials"
        />
        <PartialValue
          label="Password Last Used"
          valuePath="password_last_used"
          errorPath={[
            'unused_credentials',
            'password_last_used',
          ]}
          renderValue={formatDate}
        />
        <PartialValue
          label="Password Last Changed"
          valuePath="password_last_changed"
          renderValue={formatDate}
        />
        <PartialValue
          label="MFA"
          valuePath="mfa_active"
        />
        <PartialValue
          label="Hardware MFA Active"
          valuePath="mfa_active_hardware"
          renderValue={value => value.toString()}
        />
        <PartialValue
          label="Access Key 1 Active"
          valuePath="access_key_1_active"
          errorPath={[
            'unused_credentials',
            'access_key_1_active',
          ]}
        />
        <PartialValue
          label="Access Key 1 Last Used"
          valuePath="access_key_1_last_used_date"
          errorPath={[
            'unused_credentials',
            'unused_access_key',
          ]}
          renderValue={formatDate}
        />
        <PartialValue
          label="Access Key 1 Last Rotated"
          valuePath="access_key_1_last_rotated"
          renderValue={formatDate}
        />
        <PartialValue
          label="Access Key 2 Active"
          valuePath="access_key_2_active"
          errorPath={[
            'unused_credentials',
            'access_key_2_active',
          ]}
        />
        <PartialValue
          label="Access Key 2 Last Used"
          valuePath="access_key_2_last_used_date"
          errorPath={[
            'unused_credentials',
            'unused_access_key',
          ]}
          renderValue={formatDate}
        />
        <PartialValue
          label="Access Key 2 Last Rotated"
          valuePath="access_key_2_last_rotated"
          renderValue={formatDate}
        />
        <PartialValue
          label="Signing Cert 1 Active"
          valuePath="cert_1_active"
        />
        <PartialValue
          label="Signing Cert 2 Active"
          valuePath="cert_2_active"
        />
      </div>
    </Partial>
  );
};

IamCredentialReport.propTypes = propTypes;

export default IamCredentialReport;
