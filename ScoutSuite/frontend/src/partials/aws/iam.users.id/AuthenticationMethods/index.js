import React from 'react';
import PropTypes from 'prop-types';
import get from 'lodash/get';
import isEmpty from 'lodash/isEmpty';

import {
  convertBoolToYesOrNo, 
  formatDate,
} from '../../../../utils/Partials';
import { PartialValue } from '../../../../components/Partial';
import DetailedValue from '../../../../components/DetailedValue';

import './style.scss';
import WarningMessage from '../../../../components/WarningMessage';


const propTypes = {
  mfaDevices: PropTypes.array.isRequired,
  accessKeys: PropTypes.array.isRequired,
  loginProfile: PropTypes.object.isRequired,
};


const AuthenticationMethods = props => {
  const { 
    mfaDevices, 
    accessKeys,
    loginProfile,
  } = props;

  return (
    <div className="authentication-methods">
      <PartialValue
        label="Password enabled"
        valuePath="LoginProfile"
        renderValue={value => convertBoolToYesOrNo(!isEmpty(value))}
      />
      <PartialValue
        label="Multi-Factor enabled"
        valuePath="MFADevices"
        errorPath="mfa_enabled"
        renderValue={value => convertBoolToYesOrNo(!isEmpty(value))}
      />
      {!isEmpty(mfaDevices) && (
        <ul>
          {mfaDevices.map((mfa, i) => (
            <li key={i}>
              <DetailedValue 
                label="Serial Number"
                value={mfa.SerialNumber}
              />
            </li>
          ))}
        </ul>
      )}
      <PartialValue
        label="Access Keys"
        valuePath="AccessKeys"
        errorPath="multiple_api_keys"
        renderValue={value => get(value, 'length', 0)}
      />
      {!isEmpty(accessKeys) && (
        <ul>
          {accessKeys.map((key, i) => (
            <li key={i}>
              <PartialValue
                errorPath={`AccessKey.${i}`}
                renderValue={() => (
                  <ul className="key-infos">
                    {key.AccessKeyId}
                    <li>{key.Status}</li>
                    <li>{`Created on ${formatDate(key.CreateDate)}`}</li>
                  </ul>
                )}
              />
            </li>
          ))}
        </ul>
      )}

      <div className="warnings">
        {!isEmpty(loginProfile) && accessKeys.length > 0 && (
          <PartialValue
            errorPath="password_and_keys"
            renderValue={() => (
              <WarningMessage 
                message="Review the need for password-based and key-based authentication" 
              />
            )}
          />
        )}
        {accessKeys.length > 1 && (
          <PartialValue 
            errorPath="multiple_active_api_keys"
            renderValue={() => (
              <WarningMessage 
                message="Review the need for multiple active access keys" 
              />
            )}
          />
        )}
      </div>
    </div>
  );
};

AuthenticationMethods.propTypes = propTypes;

export default AuthenticationMethods;
