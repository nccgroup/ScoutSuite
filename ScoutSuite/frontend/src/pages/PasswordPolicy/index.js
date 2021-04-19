import React from 'react';
import PropTypes from 'prop-types';
import { useParams } from 'react-router-dom';

import { useAPI } from '../../api/useAPI';
import { getPasswordPolicyEndpoint } from '../../api/paths';
import { Partial, PartialValue } from '../../components/Partial';
import Breadcrumb from '../../components/Breadcrumb';
import WarningMessage from '../../components/WarningMessage';

import './style.scss';


const propTypes = {
  findingData: PropTypes.object,
};

const defaultProps = {
  findingData: {
    path_to_issues: [],
  },
};

const PasswordPolicy = props => {
  const { findingData } = props;

  const { service } = useParams();
  const { data, loading } = useAPI(getPasswordPolicyEndpoint(service), {});
  
  if (loading) return null;
  
  return (
    <Partial 
      data={{
        item: data,
        ...findingData,
      }}
    >
      <Breadcrumb />
      <div className="password-policy">
        <h2>Password Policy</h2>
        <hr/>
        <div className="informations-card">
          <PartialValue
            label="Minimum password length"
            valuePath="MinimumPasswordLength"
          />
          {data.MinimumPasswordLength == 1 && (
            <WarningMessage 
              message="It should be noted that 1 character passwords are authorized when no password policy exists, even though the web console displays '6'"
            />
          )}
          <PartialValue
            label="Require at least one uppercase letter"
            valuePath="RequireUppercaseCharacters"
          />
          <PartialValue
            label="Require at least one lowercase letter"
            valuePath="RequireLowercaseCharacters"
          />
          <PartialValue
            label="Require at least one number"
            valuePath="RequireNumbers"
          />
          <PartialValue
            label="Require at least one non-alphanumeric character"
            valuePath="RequireSymbols"
          />
          <PartialValue
            label="Enable password expiration"
            valuePath="ExpirePasswords"
          />
          <PartialValue
            label="Password expiration period (in days)"
            valuePath="MaxPasswordAge"
          />

          <PartialValue
            label="Prevent password reuse"
            valuePath="PasswordReusePrevention"
          />
          {data.PreviousPasswordPrevented && (
            <>
              <PartialValue
                label="Number of passwords to remember"
                valuePath="PreviousPasswordPrevented"
              />
              <PartialValue
                label="Allow users to change their own password"
                valuePath="AllowUsersToChangePassword"
              />
              <PartialValue
                label="Allow users to set a new password after their password has expired"
                valuePath="HardExpiry"
              />
            </>
          )}
        </div>
      </div>
    </Partial>
  );
};

PasswordPolicy.propTypes = propTypes;
PasswordPolicy.defaultProps = defaultProps;

export default PasswordPolicy;
