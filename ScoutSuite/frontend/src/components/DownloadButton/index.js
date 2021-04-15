import React from 'react';
import GetAppOutlinedIcon from '@material-ui/icons/GetAppOutlined';
import { Button } from '@material-ui/core';
import { PropTypes } from 'prop-types';

import './style.scss';

const propTypes = {
  service: PropTypes.string.isRequired,
  resource: PropTypes.string.isRequired,
  type: PropTypes.string.isRequired,
};

const DownloadButton = ({ service, resource, type }) => {
  return (
    <form
      method="get"
      action={`http://localhost:5000/api/services/${service}/resources/${resource}/download`}
    >
      <input 
        type="hidden" name="type" 
        value={type} 
      />
      <Button
        className="download-btn"
        variant="outlined"
        type="submit"
        size="normal"
        startIcon={<GetAppOutlinedIcon />}
      >
        {type.toUpperCase()}
      </Button>
    </form>
  );
};

DownloadButton.propTypes = propTypes;

export default DownloadButton;
