import { Link, useParams } from '@reach/router';
import React from 'react';
import Layout from '../../layout';
// import PropTypes from 'prop-types';

import './style.scss';

const propTypes = {};

const Resources = () => {
  const params = useParams();

  return (
    <Layout>
      <div>
        <h3>Resources page</h3>
        <ul>
          <li>Service: {params.service}</li>
          <li>Finding: <Link to={`/services/${params.service}/findings`}>{params.finding}</Link></li>
          {!params.item && <li><Link to="an-item">Show Item detail</Link></li>}
          {params.item && <li>Item: {params.item}</li>}
        </ul>
      </div>
    </Layout>
    
  );
};

Resources.propTypes = propTypes;

export default Resources;
