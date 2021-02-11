import { useParams, Link } from '@reach/router';
import React from 'react';
import Layout from '../../layout';
// import PropTypes from 'prop-types';

import './style.scss';

const propTypes = {};

const Findings = () => {
  const params = useParams();

  return (
    <Layout>
      <div>
        <h3>Findings page</h3>
        <ul>
          <li>Service: {params.service}</li>
          <li><Link to="s3-bucket-AllUsers-read/items" >Go to items list</Link></li>
        </ul>
      </div>
    </Layout>
  );
};

Findings.propTypes = propTypes;

export default Findings;
