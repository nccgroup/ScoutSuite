import { useParams, useLocation } from 'react-router-dom';
import React from 'react';

import Provider from './Provider';
import Service from './Service';
import Findings from './Findings';
import Resources from './Resources';
import Permissions from './Permissions';
import PasswordPolicy from './PasswordPolicy/index';
import ErrorBoundary from '../ErrorBoundary';

import './style.scss';

const Breadcrumb = () => {
  const params = useParams();
  const { pathname } = useLocation();

  return (
    <ErrorBoundary>
      <div className="breadcrumb-nav">
        <Provider />
        {params.category && <Service service={params.category} />}
        {params.service && <Service service={params.service} />}
        {params.finding && <Findings service={params.service} finding={params.finding} />}
        {params.resource && <Resources service={params.service} resource={params.resource} />}
        {pathname.includes('/permissions/') && <Permissions service={params.service} id={params.id} />}
        {pathname.includes('/password_policy/') && <PasswordPolicy service={params.service} id={params.id} />}
      </div>
    </ErrorBoundary>
  );
};

export default Breadcrumb;
