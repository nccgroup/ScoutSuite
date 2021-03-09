import { Link, useParams } from '@reach/router';
import React from 'react';
// import PropTypes from 'prop-types';

import Breadcrumb from '../../components/Breadcrumb/index';

import './style.scss';

const propTypes = {};

const Resources = () => {
  const params = useParams();

  return (
    <>
      <Breadcrumb />
      <div>
        <h3>Resources page</h3>
        <ul>
          <li>Service: {params.service}</li>
          <li>Finding: <Link to={`/services/${params.service}/findings`}>{params.finding}</Link></li>
          {!params.item && <li><Link to="an-item">Show Item detail</Link></li>}
          {params.item && <li>Item: {params.item}</li>}
        </ul>
      </div>
    </>
    
  );
};

Resources.propTypes = propTypes;

export default Resources;
