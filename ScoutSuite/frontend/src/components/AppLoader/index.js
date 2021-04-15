import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { PropTypes } from 'prop-types';
import CircularProgress from '@material-ui/core/CircularProgress';

import { BASE_URL } from '../../api/api';

import './style.scss';

const propTypes = {
  children: PropTypes.node.isRequired
};

const AppLoader = props => {
  const { children } = props;
  const [health, setHealth] = useState(false);
  
  const checkHealth = async () => {
    try {
      const { data } = await axios.get(BASE_URL + '/health');
      setHealth(data === 'OK');
    } catch (err) {
      setTimeout(async () => await checkHealth(), 1000);
    }
  };

  useEffect(() => {
    checkHealth();
  }, []);

  if (health) {
    return children;
  }

  return <div className="app-loader">
    <div>
      <CircularProgress />

      <div className="delay-explanation">
        <h3>Is the server running?</h3>
        <p>You need to start the server using <code>python scout.py PROVIDER</code> to generate a report and start the server OR run <code>python scout.py PROVIDER --server-only PATH_TO_JSON_REPORT_FILE.json</code> if you already have a report.</p>
        <p>You can then view the web report at <a href="http://localhost:5000"><code>http://localhost:5000</code></a>.</p>
      </div>

    </div>
  </div>;
};

AppLoader.propTypes = propTypes;

export default AppLoader;
