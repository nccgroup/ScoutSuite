import { useParams } from '@reach/router';
import React from 'react';

import Provider from './Provider';
import Service from './Service';
import Findings from './Findings';
import Resources from './Resources';

import './style.scss';

const Breadcrumb = () => {
  const params = useParams();

  return (
    <div className="breadcrumb-nav">
      <Provider />
      {params.service && <Service service={params.service} />}
      {params.finding && <Findings service={params.service} finding={params.finding} />}
      {params.resource && <Resources service={params.service} resource={params.resource} />}
    </div>
  );
};

export default Breadcrumb;
