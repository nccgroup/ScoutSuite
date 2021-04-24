import React from 'react';
import { useParams } from 'react-router-dom';
import get from 'lodash/get';

import { useAPI } from '../../api/useAPI';
import { getRawEndpoint } from '../../api/paths';
import PasswordPolicy from '../PasswordPolicy';


const PasswordPolicyFinding = () => {
  const { service, id } = useParams();  

  const { data, loading } = useAPI(
    getRawEndpoint(`services.${service}.findings.${id}`)
  );

  if (loading) return null;
  
  const issues = get(data, 'items', []);

  return (
    <PasswordPolicy 
      findingData={{
        path: `${service}.password_policy`,
        path_to_issues: issues.map(issue => issue.split('.').pop()),
        level: data.level,
      }}
    />
  );
};

export default PasswordPolicyFinding;
