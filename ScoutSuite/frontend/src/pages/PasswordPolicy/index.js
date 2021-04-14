import React from 'react';
import { useParams, useLocation } from 'react-router-dom';
import get from 'lodash/get';

import { useAPI } from '../../api/useAPI';
import { 
  getPasswordPolicyEndpoint,
  getRawEndpoint,
} from '../../api/paths';
import { Partial, PartialValue } from '../../components/Partial';
import Breadcrumb from '../../components/Breadcrumb';

import './style.scss';


const PasswordPolicy = () => {
  const { service } = useParams();
  const { data, loading: l1 } = useAPI(getPasswordPolicyEndpoint(service), {});
  
  const finding = new URLSearchParams(useLocation().search).get('finding');

  const { data: findingData, loading: l2 } = useAPI(
    getRawEndpoint(`services.${service}.findings.${finding}`)
  );
  
  if (l1 || l2) return null;

  const issues = get(findingData, 'items', []);

  return (
    <Partial 
      data={{
        item: data,
        path: `${service}.password_policy`,
        path_to_issues: issues.map(issue => issue.split('.').pop()),
        level: findingData.level,
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

export default PasswordPolicy;
