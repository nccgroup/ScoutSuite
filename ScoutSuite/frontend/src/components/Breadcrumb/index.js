import { useParams } from '@reach/router';
import React from 'react';

import Provider from './Provider';
import Service from './Service';
import Findings from './Findings';

import './style.scss';

const Breadcrumb = () => {
  const params = useParams();

  return (
    <div className="breadcrumb-nav">
      <Provider />
      {params.service && <Service service={params.service} />}
      {params.finding && <Findings service={params.service} finding={params.finding} />}
    </div>
  );
};

export default Breadcrumb;
