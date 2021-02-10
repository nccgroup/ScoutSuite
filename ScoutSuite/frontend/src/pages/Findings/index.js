import { useParams, Link } from '@reach/router';
import React from 'react';
// import PropTypes from 'prop-types';

import './style.scss';

const propTypes = {};

const Findings = () => {
  const params = useParams();

  return (
    <div>
      <h3>Findings page</h3>
      <ul>
        <li>Service: {params.service}</li>
        <li><Link to="a-finding-test/items" >Go to items list</Link></li>
      </ul>
    </div>
  );
};

Findings.propTypes = propTypes;

export default Findings;
